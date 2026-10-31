const planForm = document.getElementById("planForm");
const submitBtn = document.getElementById("submitBtn");
const errorBox = document.getElementById("formError");

function addItems(elementId, items) {
  const list = document.getElementById(elementId);
  list.innerHTML = "";
  items.forEach(item => {
    const li = document.createElement("li");
    li.textContent = item;
    list.appendChild(li);
  });
}

planForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorBox.textContent = "";
  submitBtn.disabled = true;
  submitBtn.textContent = "Creating your plan...";
  const formData = Object.fromEntries(new FormData(planForm).entries());

  try {
    const response = await fetch("/api/plan", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(formData)
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "Could not create plan.");
    const plan = result.plan;
    document.getElementById("workoutTitle").textContent = plan.workout_title;
    addItems("workoutList", plan.workout);
    addItems("dietList", plan.diet);
    document.getElementById("levelNote").textContent = plan.level_note;
    document.getElementById("equipmentNote").textContent = plan.equipment_note;
    document.getElementById("durationNote").textContent = plan.duration_note;
    document.getElementById("focusNote").textContent = plan.focus_note;
    document.getElementById("weeklyNote").textContent = plan.weekly_note;
    const results = document.getElementById("results");
    results.hidden = false;
    results.scrollIntoView({behavior: "smooth"});
    loadHistory();
  } catch (error) {
    errorBox.textContent = error.message;
  } finally {
    submitBtn.disabled = false;
    submitBtn.innerHTML = 'Generate my plan <span>→</span>';
  }
});

async function loadHistory() {
  const container = document.getElementById("historyList");
  try {
    const response = await fetch("/api/history");
    const records = await response.json();
    container.innerHTML = "";
    if (!records.length) {
      container.innerHTML = '<p class="empty-state">Your saved plans will appear here after you create one.</p>';
      return;
    }
    records.forEach(record => {
      const item = document.createElement("div");
      item.className = "history-item";
      const name = document.createElement("strong");
      name.textContent = `${record.name} — ${record.goal.replaceAll("_", " ")}`;
      const date = document.createElement("span");
      date.textContent = new Date(record.created_at).toLocaleString();
      item.append(name, date);
      container.appendChild(item);
    });
  } catch {
    container.innerHTML = '<p class="empty-state">Could not load plan history.</p>';
  }
}
document.getElementById("refreshHistory").addEventListener("click", loadHistory);

const chatForm = document.getElementById("chatForm");
const chatText = document.getElementById("chatText");
const chatMessages = document.getElementById("chatMessages");

function addBubble(text, type) {
  const bubble = document.createElement("div");
  bubble.className = `bubble ${type}`;
  bubble.textContent = text;
  chatMessages.appendChild(bubble);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}
chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = chatText.value.trim();
  if (!message) return;
  addBubble(message, "user");
  chatText.value = "";
  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({message})
    });
    const data = await response.json();
    addBubble(data.reply, "bot");
  } catch {
    addBubble("Sorry, I could not connect. Please try again.", "bot");
  }
});
loadHistory();
