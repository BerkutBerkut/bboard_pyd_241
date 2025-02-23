const domain = "http://localhost:8000/api/";

const list = document.querySelector("#list");
const itemId = document.querySelector("#id");
const itemUser = document.querySelector("#user");
const itemEmail = document.querySelector("#email");

async function loadItem(evt) {
  evt.preventDefault();
  const result = await fetch(evt.target.href);
  if (result.ok) {
    const data = await result.json();
    itemId.value = data.id;
    itemUser.value = data.user;
    itemEmail.value = data.email;
    
  } else console.log(result.statusText);
}

async function deleteItem(evt) {
  evt.preventDefault();
  const result = await fetch(evt.target.href, { method: "DELETE" });
  if (result.ok) loadList();
  else console.log(result.statusText);
}

async function loadList() {
  const result = await fetch(`${domain}users`);

  if (result.ok) {
    const data = await result.json();
    let s = "",
      d;

    for (let i = 0; i < data.length; i++) {
      d = data[i];
      s += `<li>${d.user} 
                        <a href="${domain}users/${d.id}/" class="detail">Вывести</a>
                        <a href="${domain}users/${d.id}/" class="delete">Удалить</a>
            </li>`;
    }
    list.innerHTML = s;

    let links = list.querySelectorAll("li a.detail");
    links.forEach((link) => {
      link.addEventListener("click", loadItem);
    });

    links = list.querySelectorAll("li a.delete");
    links.forEach((link) => {
      link.addEventListener("click", deleteItem);
    });
  } else console.log(result.statusText);
}

loadList();

itemTitle.form.addEventListener("submit", async (evt) => {
  evt.preventDefault();
  let url, method;
  if (itemId.value) {
    url = `${domain}users/${itemId.value}/`;
    method = "PUT";
  } else {
    url = `${domain}users/`;
    method = "POST";
  }

  const result = await fetch(url, {
    method: method,
    body: JSON.stringify({
      user: itemUser.value,
      email: itemEmail.value,
    }),
    headers: { "Content-Type": "application/json" },
  });
  if (result.ok) {
    loadList();
    itemUser.value = "";
    itemEmail.value = "";
    itemId.value = "";
  } else console.log(result.statusText);
});
