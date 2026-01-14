
const input = document.getElementById("input");
const messages = document.getElementById("messages");

input.addEventListener("keydown", async (e) => {
  if (e.key !== "Enter") return;

  const q = input.value.trim();
  if (!q) return;            // prevent empty request

  input.value = "";
  messages.innerHTML += `<div class="user">${q}</div>`;

  try {
    const r = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: q })
    });

    if (!r.ok) {
      messages.innerHTML += `<div class="bot">Error (${r.status})</div>`;
      return;
    }

    const j = await r.json();
    messages.innerHTML += `<div class="bot">${j.answer}</div>`;
    messages.scrollTop = messages.scrollHeight;
  } catch (err) {
    messages.innerHTML += `<div class="bot">Connection error</div>`;
  }
});
