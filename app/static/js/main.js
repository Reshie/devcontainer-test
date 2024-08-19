'use strict';

const FASTAPI_URL = 'http://127.0.0.1:8080';

document.addEventListener('DOMContentLoaded', () => {
  const todoForm = document.getElementById('todo-form');
  const todoInput = document.getElementById('todo-input');
  const todoList = document.getElementById('todo-list');

  // 追加ボタン
  todoForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const todoText = todoInput.value.trim();
    if (todoText !== '') {
      createTask(todoText).then((task) => {
        addTodoItem(task.title, task.id);
      });
      todoInput.value = '';
    }
  });

  // DBからタスクの取得
  getTasks().then((tasks) => {
    tasks.forEach((task) => {
      addTodoItem(task.title, task.id, task.is_done);
    });
  });

  class TodoItem {
    constructor(title, id, completed = false) {
      this.title = title;
      this.id = id;
      this.completed = completed;
    }

    render() {
      const li = document.createElement('li');
      const checkbox = document.createElement('input');

      li.classList.toggle('completed', this.completed);
      checkbox.type = 'checkbox';
      checkbox.checked = this.completed;
      checkbox.addEventListener('change', () => {
        toggleTask(this.id).then((task) => {
          li.classList.toggle('completed', task.is_done);
        });
      });

      const span = document.createElement('span');
      span.textContent = this.title;
      span.classList.add('task-text');
      span.addEventListener('click', () => {
        toggleTask(this.id).then((task) => {
          checkbox.checked = task.is_done;
          li.classList.toggle('completed', task.is_done);
        });
      });

      const deleteButton = document.createElement('button');
      deleteButton.textContent = '削除';
      deleteButton.addEventListener('click', () => {
        deleteTask(this.id).then(() => {
          li.remove();
        });
      });

      li.appendChild(checkbox);
      li.appendChild(span);
      li.appendChild(deleteButton);
      todoList.appendChild(li);
    }
  }

  function addTodoItem(title, id, completed = false) {
    const todoItem = new TodoItem(title, id, completed);
    todoItem.render();
  }
});

async function getTasks() {
  try {
    const response = await fetch(`${FASTAPI_URL}/task`);

    if (!response.ok) {
      throw new Error(`タスクの取得に失敗しました: ${response.status}`);
    }

    const tasks = await response.json();
    return tasks;
  } catch (e) {
    console.error('エラーが発生しました: ', e);
  }
}

async function createTask(title) {
  try {
    const response = await fetch(`${FASTAPI_URL}/task`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ title }),
    });

    if (!response.ok) {
      throw new Error(`タスクの作成に失敗しました: ${response.status}`);
    }

    const task = await response.json();
    return task;
  } catch (e) {
    console.error('エラーが発生しました: ', e);
  }
}

async function toggleTask(taskId) {
  try {
    const response = await fetch(`${FASTAPI_URL}/task/${taskId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
      body: JSON.stringify({ taskId }),
    });

    if (!response.ok) {
      throw new Error(`タスクの更新に失敗しました: ${response.status}`);
    }

    const task = await response.json();
    return task;
  } catch (e) {
    console.error('エラーが発生しました: ', e);
  }
}

async function deleteTask(taskId) {
  try {
    const response = await fetch(`${FASTAPI_URL}/task/${taskId}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      throw new Error(`タスクの削除に失敗しました: ${response.status}`);
    }

    return response.ok;
  } catch (e) {
    console.error('エラーが発生しました: ', e);
  }
}