document.addEventListener('DOMContentLoaded', () => {
  const todoForm = document.getElementById('todo-form');
  const todoInput = document.getElementById('todo-input');
  const todoList = document.getElementById('todo-list');

  todoForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const todoText = todoInput.value.trim();
    if (todoText !== '') {
      addTodoItem(todoText);
      todoInput.value = '';
    }
  });

  function addTodoItem(text) {
    const li = document.createElement('li');
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.addEventListener('change', () => {
      li.classList.toggle('completed', checkbox.checked);
    });

    const span = document.createElement('span');
    span.textContent = text;
    span.classList.add('task-text');
    span.addEventListener('click', () => {
      checkbox.checked = !checkbox.checked;
      li.classList.toggle('completed', checkbox.checked);
    });

    const deleteButton = document.createElement('button');
    deleteButton.textContent = '削除';
    deleteButton.addEventListener('click', () => {
      li.remove();
    });

    li.appendChild(checkbox);
    li.appendChild(span);
    li.appendChild(deleteButton);
    todoList.appendChild(li);
  }
});