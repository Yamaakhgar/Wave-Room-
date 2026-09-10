
const statusText = document.getElementById("statusText");

function toast(text) {
  const old = document.querySelector(".toast");
  if (old) old.remove();
  const el = document.createElement("div");
  el.className = "toast";
  el.textContent = text;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 2500);
}

async function joinRoom(id, button) {
  const res = await fetch(`/api/rooms/${id}/join`, { method: "POST" });
  const data = await res.json();

  if (!res.ok) {
    toast(data.error || "Could not join room");
    return;
  }

  button.textContent = "Joined ✓";
  button.disabled = true;

  const card = button.closest(".room-card");
  card.querySelector(".listeners").textContent =
    `🎧 ${data.room.listeners} listening`;

  statusText.textContent = data.message;
  toast(data.message);
}

document.getElementById("roomForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const name = document.getElementById("roomName").value.trim();
  const topic = document.getElementById("roomTopic").value.trim();

  const res = await fetch("/api/rooms", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, topic })
  });

  const room = await res.json();

  if (!res.ok) {
    toast(room.error || "Could not create room");
    return;
  }

  const grid = document.getElementById("roomsGrid");
  const card = document.createElement("article");
  card.className = "room-card";
  card.dataset.roomId = room.id;

  card.innerHTML = `
    <div class="room-top">
      <img src="/static/images/avatar4.png" alt="Host">
      <div>
        <h4>${escapeHtml(room.name)}</h4>
        <p>Hosted by ${escapeHtml(room.host)}</p>
      </div>
      <span class="live-dot">LIVE</span>
    </div>
    <p class="topic">${escapeHtml(room.topic)}</p>
    <div class="room-bottom">
      <span class="listeners">🎧 ${room.listeners} listening</span>
      <button class="join-btn" onclick="joinRoom(${room.id}, this)">Join</button>
    </div>
  `;

  grid.prepend(card);
  e.target.reset();
  statusText.textContent = `Room "${room.name}" created`;
  toast("Room created successfully 🎙️");
});

async function loadMessages() {
  const res = await fetch("/api/messages");
  const items = await res.json();
  const box = document.getElementById("messages");

  box.innerHTML = items.map(m => `
    <div class="message">
      <strong>${escapeHtml(m.user)}</strong>
      <div>${escapeHtml(m.text)}</div>
      <small>${escapeHtml(m.time)}</small>
    </div>
  `).join("");

  box.scrollTop = box.scrollHeight;
}

document.getElementById("messageForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const input = document.getElementById("messageText");
  const text = input.value.trim();

  const res = await fetch("/api/messages", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text })
  });

  const msg = await res.json();
  if (!res.ok) {
    toast(msg.error || "Could not send message");
    return;
  }

  input.value = "";
  await loadMessages();
});

document.getElementById("themeBtn").addEventListener("click", () => {
  document.body.classList.toggle("light");
});

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

loadMessages();
