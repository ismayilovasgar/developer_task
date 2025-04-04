const createForm = document.getElementById("createForm");

document.addEventListener("DOMContentLoaded", function () {
  fetchTasks();
});

function fetchTasks() {
  fetch("api/v2/tasks/", {
    method: "GET",
  }) // API'ni buraya ekle
    .then((response) => response.json())
    .then((data) => {
      const taskList = document.getElementById("task-list");
      taskList.innerHTML = ""; 

      data.forEach((task) => {
        const taskHtml = `
                <div class="list-group-item list-group-item-action task-item d-flex flex-column" data-bs-toggle="collapse" data-bs-target="#task${
                  task.id
                }">
                    <div class="d-flex justify-content-between align-items-center flex-wrap">
                        <span style="min-width:80px;" class="badge ${
                          task.status === "completed"
                            ? "bg-success"
                            : "bg-warning"
                        }">
                            ${
                              task.status_display
                              // task.status.charAt(0).toUpperCase() +
                              // task.status.slice(1)
                            }
                        </span>
                        <span class="flex-grow-1 text-center">${
                          task.title
                        }</span>
                        <span class="text-muted mx-2">${
                          task.created_at_pretty
                        }</span>
                        <div class="d-flex gap-2">
                            <button class="btn btn-sm btn-primary" onclick="openUpdateModal(${
                              task.id
                            }, '${task.title}', '${task.content}','${task.status}')">Yenilə</button>
                            <button class="btn btn-sm btn-danger" onclick="openDeleteModal(${
                              task.id
                            })">Sil</button>
                        </div>
                    </div>
                    <div id="task${task.id}" class="collapse mt-2">
                        <p class="mb-0">${task.content}</p>
                    </div>
                </div>
            `;
        taskList.innerHTML += taskHtml;
      });
    })
    .catch((error) => console.error("Error fetching tasks:", error));
}

// DELETE MODAL
let deleteTaskId = null;

function openDeleteModal(taskId) {
  deleteTaskId = taskId;
  new bootstrap.Modal(document.getElementById("deleteModal")).show();
}

document.getElementById("confirmDelete").addEventListener("click", function () {
  if (deleteTaskId) {
    fetch(`api/v2/tasks/delete/${deleteTaskId}/`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
    })
      .then((response) => {
        if (response.ok) {
          fetchTasks();
          bootstrap.Modal.getInstance(
            document.getElementById("deleteModal")
          ).hide();
        } else {
          alert("Failed to delete task.");
        }
      })
      .catch((error) => console.error("Error deleting task:", error));
  }
});

// UPDATE MODAL
function openUpdateModal(taskId, title, content,status) {
  document.getElementById("updateTaskId").value = taskId;
  document.getElementById("updateTitle").value = title;
  document.getElementById("updateDescription").value = content;
  document.getElementById("taskTypeUpdateForm").value = status;
  new bootstrap.Modal(document.getElementById("updateModal")).show();
}

document
  .getElementById("updateForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const taskId = document.getElementById("updateTaskId").value;
    const updatedTitle = document.getElementById("updateTitle").value;
    const updatedDescription =
      document.getElementById("updateDescription").value;
    const updatedStatus = document.getElementById("taskTypeUpdateForm").value;

    fetch(`api/v2/tasks/update/${taskId}/`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({
        title: updatedTitle,
        content: updatedDescription,
        status: updatedStatus,
      }),
    })
      .then((response) => response.json())
      .then(() => {
        fetchTasks();
        bootstrap.Modal.getInstance(
          document.getElementById("updateModal")
        ).hide();
      })
      .catch((error) => console.error("Error updating task:", error));
  });

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// ********************************************
// Yeni Görev Ekle Modal'ını açmak için
function openCreateModal() {
  const createModal = new bootstrap.Modal(
    document.getElementById("createModal")
  );
  createModal.show();
}

// **************** Filter *******************************
// Filtreleme işlemi
function filterTasks(status) {
  const url = `api/v2/tasks/?status=${status}`; // Sorgu parametresi ile URL oluşturuluyor

  // Fetch ile veriyi çekiyoruz
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      // Yeni veriyi işleyip, listeyi güncelle
      updateTaskList(data);
    })
    .catch((error) => console.error("Error fetching tasks:", error));
}

// Görev listesine gelen veriyi eklemek
function updateTaskList(tasks) {
  const taskList = document.getElementById("task-list");
  taskList.innerHTML = ""; // Listeyi temizle

  tasks.forEach((task) => {
    // Yeni task div elementini oluşturuyoruz
    const taskElement = document.createElement("div");
    taskElement.classList.add(
      "list-group-item",
      "list-group-item-action",
      "task-item",
      "d-flex",
      "flex-column"
    );
    taskElement.setAttribute("data-bs-toggle", "collapse");
    taskElement.setAttribute("data-bs-target", `#task${task.id}`); // Collapse ile gizlenebilir

    // HTML içeriği
    taskElement.innerHTML = `
          <div class="d-flex justify-content-between align-items-center flex-wrap">
              <span style="min-width:80px;" class="badge ${
                task.status === "completed" ? "bg-success" : "bg-warning"
              }">
                  ${task.status_display}
              </span>
              <span class="flex-grow-1 text-center">${task.title}</span>
              <span class="text-muted mx-2">${task.created_at_pretty}</span>
              <div class="d-flex gap-2">
                  <button class="btn btn-sm btn-primary" onclick="openUpdateModal(${
                    task.id
                  }, '${task.title}', '${task.content}')">Yenilə</button>
                  <button class="btn btn-sm btn-danger" onclick="openDeleteModal(${
                    task.id
                  })">Sil</button>
              </div>
          </div>
          <div id="task${task.id}" class="collapse mt-2">
              <p class="mb-0">${task.content}</p>
          </div>
      `;

    // Task öğesini listeye ekle
    taskList.appendChild(taskElement);
  });
}

// ********************** add new task **********************************

document
  .getElementById("createForm")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Sayfanın yenilenmesini engelle

    const title = document.getElementById("createTitle").value;
    const description = document.getElementById("createDescription").value;
    const taskType = document.getElementById("taskType").value;

    fetch("/api/v2/tasks/create/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({
        title: title,
        content: description,
        status: taskType,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.id) {
          updateTaskList([data]);
          const createModal = bootstrap.Modal.getInstance(
            document.getElementById("createModal")
          );
          createModal.hide(); // Modalı kapat
          // const createForm = document.getElementById("createForm");
          document
            .getElementById("createModal")
            .addEventListener("hidden.bs.modal", function () {
              createForm.reset(); // Formun bütün inputlarını sıfırla
            });
        } else {
          alert("Bir hata oluştu, lütfen tekrar deneyin.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("Görev oluşturulurken bir hata oluştu.");
      });
  });
