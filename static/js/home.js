// document.addEventListener("DOMContentLoaded", function () {
//   fetchTasks();
// });

// function fetchTasks() {
//   fetch("api/v1/tasks/", {
//     method: "GET",
//   })
//     .then((response) => response.json())
//     .then((data) => {
//       const listGroup = document.querySelector(".list-group");
//       listGroup.innerHTML = "";

//       data.forEach((task) => {
//         const taskHtml = `
//                 <div class="list-group-item list-group-item-action task-item d-flex flex-column" data-bs-toggle="collapse" data-bs-target="#task${
//                   task.id
//                 }">
//                     <div class="d-flex justify-content-between align-items-center flex-wrap">
//                         <span class="badge ${
//                           task.status === "completed"
//                             ? "bg-success"
//                             : "bg-warning"
//                         }">
//                             ${
//                               task.status.charAt(0).toUpperCase() +
//                               task.status.slice(1)
//                             }
//                         </span>
//                         <span class="flex-grow-1 text-center">${
//                           task.title
//                         }</span>
//                         <span class="text-muted  mx-2">${task.created_at_pretty}</span>
//                         <div class="d-flex gap-2">
//                             <button class="btn btn-sm btn-primary" onclick="updateTask(${
//                               task.id
//                             })">Update</button>
//                             <button class="btn btn-sm btn-danger" onclick="deleteTask(${
//                               task.id
//                             })">Delete</button>
//                         </div>
//                     </div>
//                     <div id="task${task.id}" class="collapse mt-2">
//                         <p class="mb-0">${task.content}</p>
//                     </div>
//                 </div>
//             `;
//         listGroup.innerHTML += taskHtml;
//       });
//     })
//     .catch((error) => console.error("Error fetching tasks:", error));
// }

// function updateTask(taskId) {
//   alert(`Update task: ${taskId}`); // Güncelleme mantığını burada ekleyebilirsin
// }

// function deleteTask(taskId) {
//   if (confirm("Are you sure you want to delete this task?")) {
//     fetch(`api/v1/tasks/${taskId}`, {
//       method: "DELETE",
//     })
//       .then((response) => {
//         if (response.ok) {
//           fetchTasks(); // Silme işleminden sonra listeyi güncelle
//         } else {
//           alert("Failed to delete task.");
//         }
//       })
//       .catch((error) => console.error("Error deleting task:", error));
//   }
// }

document.addEventListener("DOMContentLoaded", function () {
  fetchTasks();
});

function fetchTasks() {
  fetch("api/v1/tasks/", {
    method: "GET",
  }) // API'ni buraya ekle
    .then((response) => response.json())
    .then((data) => {
      const taskList = document.getElementById("task-list");
      taskList.innerHTML = ""; // Önce listeyi temizle

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
                            ${
                              task.status.charAt(0).toUpperCase() +
                              task.status.slice(1)
                            }
                        </span>
                        <span class="flex-grow-1 text-center">${
                          task.title
                        }</span>
                        <span class="text-muted mx-2">${task.created_at_pretty}</span>
                        <div class="d-flex gap-2">
                            <button class="btn btn-sm btn-primary" onclick="openUpdateModal(${
                              task.id
                            }, '${task.title}', '${
          task.content
        }')">Update</button>
                            <button class="btn btn-sm btn-danger" onclick="openDeleteModal(${
                              task.id
                            })">Delete</button>
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
    fetch(`api/v1/tasks/${deleteTaskId}/`, {
      method: "DELETE",
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

    fetch(`api/v1/tasks/${taskId}/`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title: updatedTitle,
        content: updatedDescription,
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
