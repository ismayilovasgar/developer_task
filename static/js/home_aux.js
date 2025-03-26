const createForm = document.getElementById("createForm");

document.addEventListener("DOMContentLoaded", function () {
  fetchTasks();
});

function fetchTasks() {
  fetch("api/v2/tasks/", {
    method: "GET",
  })
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
                        <span class="badge ${
                          task.status === "completed"
                            ? "bg-success"
                            : "bg-warning"
                        }">
                            ${task.status_display}
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
                            }, '${task.title}', '${
          task.content
        }')">Yenilə</button>
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
    .catch((error) => console.error("Tapşırıqları yükləyərkən xəta:", error));
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
          alert("Tapşırığı silmək mümkün olmadı.");
        }
      })
      .catch((error) => console.error("Tapşırığı silarkən xəta:", error));
  }
});

// UPDATE MODAL
function openUpdateModal(taskId, title, content) {
  document.getElementById("updateTaskId").value = taskId;
  document.getElementById("updateTitle").value = title;
  document.getElementById("updateDescription").value = content;
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
      .catch((error) => console.error("Tapşırığı yeniləyərkən xəta:", error));
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

function openCreateModal() {
  const createModal = new bootstrap.Modal(
    document.getElementById("createModal")
  );
  createModal.show();
}

function filterTasks(status) {
  const url = `api/v2/tasks/?status=${status}`;

  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      updateTaskList(data);
    })
    .catch((error) => console.error("Tapşırıqları filtləyərkən xəta:", error));
}

function updateTaskList(tasks) {
  const taskList = document.getElementById("task-list");
  taskList.innerHTML = "";

  tasks.forEach((task) => {
    const taskElement = document.createElement("div");
    taskElement.classList.add(
      "list-group-item",
      "list-group-item-action",
      "task-item",
      "d-flex",
      "flex-column"
    );
    taskElement.setAttribute("data-bs-toggle", "collapse");
    taskElement.setAttribute("data-bs-target", `#task${task.id}`);

    taskElement.innerHTML = `
          <div class="d-flex justify-content-between align-items-center flex-wrap">
              <span class="badge ${
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

    taskList.appendChild(taskElement);
  });
}

document
  .getElementById("createForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();

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
          createModal.hide();
          document
            .getElementById("createModal")
            .addEventListener("hidden.bs.modal", function () {
              createForm.reset();
            });
        } else {
          alert("Bir xəta baş verdi, zəhmət olmasa yenidən cəhd edin.");
        }
      })
      .catch((error) => {
        console.error("Xəta:", error);
        alert("Tapşırıq yaradılarkən xəta baş verdi.");
      });
  });

// ****************************************************************************
// // Utility Helper Sınıfı
// class AppUtils {
//   static getCookie(name) {
//     const cookieArr = document.cookie.split(";");
//     for (let cookie of cookieArr) {
//       const [cookieName, cookieValue] = cookie.trim().split("=");
//       if (cookieName === name) {
//         return decodeURIComponent(cookieValue);
//       }
//     }
//     return null;
//   }

//   static showToast(message, type = "info") {
//     // Toast bildirimi için bootstrap toast kullanılabilir
//     console.log(`[${type.toUpperCase()}] ${message}`);
//   }
// }

// // Görev Servisi
// class TaskService {
//   static async fetchTasks(status = "") {
//     try {
//       const url = status ? `api/v2/tasks/?status=${status}` : "api/v2/tasks/";

//       const response = await fetch(url);

//       if (!response.ok) {
//         throw new Error("Görevler yüklenemedi");
//       }

//       return await response.json();
//     } catch (error) {
//       AppUtils.showToast("Görevler yüklenirken hata oluştu", "danger");
//       console.error("Görev yükleme hatası:", error);
//       return [];
//     }
//   }

//   static async createTask(taskData) {
//     try {
//       const response = await fetch("/api/v2/tasks/create/", {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//           "X-CSRFToken": AppUtils.getCookie("csrftoken"),
//         },
//         body: JSON.stringify(taskData),
//       });

//       if (!response.ok) {
//         throw new Error("Görev oluşturulamadı");
//       }

//       const data = await response.json();
//       AppUtils.showToast("Görev başarıyla oluşturuldu", "success");
//       return data;
//     } catch (error) {
//       AppUtils.showToast("Görev oluşturulurken hata oluştu", "danger");
//       console.error("Hata:", error);
//       return null;
//     }
//   }
// }

// // Görev Arayüzü Yönetimi
// class TaskUI {
//   static renderTaskList(tasks) {
//     const taskList = document.getElementById("task-list");
//     taskList.innerHTML = "";

//     tasks.forEach((task) => {
//       const taskElement = document.createElement("div");
//       taskElement.classList.add(
//         "list-group-item",
//         "list-group-item-action",
//         "task-item",
//         "d-flex",
//         "flex-column"
//       );
//       taskElement.setAttribute("data-bs-toggle", "collapse");
//       taskElement.setAttribute("data-bs-target", `#task${task.id}`);

//       taskElement.innerHTML = `
//               <div class="d-flex justify-content-between align-items-center flex-wrap">
//                   <span class="badge ${
//                     task.status === "completed" ? "bg-success" : "bg-warning"
//                   }">
//                       ${task.status_display}
//                   </span>
//                   <span class="flex-grow-1 text-center">${task.title}</span>
//                   <span class="text-muted mx-2">${task.created_at_pretty}</span>
//                   <div class="d-flex gap-2">
//                       <button class="btn btn-sm btn-primary" 
//                           onclick="openUpdateModal(${task.id}, '${
//         task.title
//       }', '${task.content}')">
//                           Güncelle
//                       </button>
//                       <button class="btn btn-sm btn-danger" 
//                           onclick="openDeleteModal(${task.id})">
//                           Sil
//                       </button>
//                   </div>
//               </div>
//               <div id="task${task.id}" class="collapse mt-2">
//                   <p class="mb-0">${task.content}</p>
//               </div>
//           `;

//       taskList.appendChild(taskElement);
//     });
//   }
// }

// // Global Fonksiyonlar
// function openCreateModal() {
//   const createModal = new bootstrap.Modal(
//     document.getElementById("createModal")
//   );
//   createModal.show();
// }

// function openUpdateModal(taskId, title, content) {
//   document.getElementById("updateTaskId").value = taskId;
//   document.getElementById("updateTitle").value = title;
//   document.getElementById("updateDescription").value = content;

//   const updateModal = new bootstrap.Modal(
//     document.getElementById("updateModal")
//   );
//   updateModal.show();
// }

// function openDeleteModal(taskId) {
//   // Global değişken kullanmak yerine doğrudan parametre geçebiliriz
//   document.getElementById("confirmDelete").onclick = () => {
//     fetch(`api/v2/tasks/delete/${taskId}/`, {
//       method: "DELETE",
//       headers: {
//         "Content-Type": "application/json",
//         "X-CSRFToken": AppUtils.getCookie("csrftoken"),
//       },
//     })
//       .then((response) => {
//         if (response.ok) {
//           fetchTasks(); // Listeyi yeniden yükle
//           bootstrap.Modal.getInstance(
//             document.getElementById("deleteModal")
//           ).hide();
//         } else {
//           AppUtils.showToast("Görev silinemedi", "danger");
//         }
//       })
//       .catch((error) => {
//         console.error("Silme hatası:", error);
//         AppUtils.showToast("Görev silinirken hata oluştu", "danger");
//       });
//   };

//   const deleteModal = new bootstrap.Modal(
//     document.getElementById("deleteModal")
//   );
//   deleteModal.show();
// }

// function filterTasks(status) {
//   TaskService.fetchTasks(status).then((tasks) => {
//     TaskUI.renderTaskList(tasks);
//   });
// }

// // Sayfa Yüklendiğinde Görevleri Getir
// function fetchTasks() {
//   TaskService.fetchTasks().then((tasks) => {
//     TaskUI.renderTaskList(tasks);
//   });
// }

// // Create Form Submit Event
// document
//   .getElementById("createForm")
//   .addEventListener("submit", async (event) => {
//     event.preventDefault();

//     const title = document.getElementById("createTitle").value;
//     const description = document.getElementById("createDescription").value;
//     const taskType = document.getElementById("taskType").value;

//     const taskData = {
//       title,
//       content: description,
//       status: taskType,
//     };

//     const newTask = await TaskService.createTask(taskData);

//     if (newTask) {
//       fetchTasks(); // Listeyi yeniden yükle
//       bootstrap.Modal.getInstance(
//         document.getElementById("createModal")
//       ).hide();
//       event.target.reset(); // Formu sıfırla
//     }
//   });

// // Sayfa Yüklendiğinde
// document.addEventListener("DOMContentLoaded", fetchTasks);
