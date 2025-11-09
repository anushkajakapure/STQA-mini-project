let todos = [];
let currentFilter = 'all';
let todoId = 1;

const todoInput = document.getElementById('todoInput');
const addBtn = document.getElementById('addBtn');
const todoList = document.getElementById('todoList');
const filterBtns = document.querySelectorAll('.filter-btn');
const clearCompletedBtn = document.getElementById('clearCompleted');

addBtn.addEventListener('click', addTodo);
todoInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') addTodo();
});

filterBtns.forEach((btn) => {
  btn.addEventListener('click', () => {
    filterBtns.forEach((b) => b.classList.remove('active'));
    btn.classList.add('active');
    currentFilter = btn.dataset.filter;
    renderTodos();
  });
});

clearCompletedBtn.addEventListener('click', clearCompleted);

function addTodo() {
  const text = todoInput.value.trim();
  if (text === '') {
    alert('Please enter a task!');
    return;
  }

  const todo = {
    id: todoId++,
    text: text,
    completed: false,
    createdAt: new Date().toISOString(),
  };

  todos.push(todo);
  todoInput.value = '';
  renderTodos();
}

function toggleTodo(id) {
  const todo = todos.find((t) => t.id === id);
  if (todo) {
    todo.completed = !todo.completed;
    renderTodos();
  }
}

function deleteTodo(id) {
  todos = todos.filter((t) => t.id !== id);
  renderTodos();
}

function clearCompleted() {
  todos = todos.filter((t) => !t.completed);
  renderTodos();
}

function renderTodos() {
  let filteredTodos = todos;

  if (currentFilter === 'active') {
    filteredTodos = todos.filter((t) => !t.completed);
  } else if (currentFilter === 'completed') {
    filteredTodos = todos.filter((t) => t.completed);
  }

  todoList.innerHTML = '';

  if (filteredTodos.length === 0) {
    todoList.innerHTML = '<div class="empty-state">No tasks to display</div>';
  } else {
    filteredTodos.forEach((todo) => {
      const li = document.createElement('li');
      li.className = `todo-item ${todo.completed ? 'completed' : ''}`;
      li.dataset.id = todo.id;

      li.innerHTML = `
        <input type="checkbox" class="todo-checkbox" ${todo.completed ? 'checked' : ''}>
        <span class="todo-text"></span>
        <button class="delete-btn">Delete</button>
      `;

      li.querySelector('.todo-text').textContent = todo.text;
      li.querySelector('.todo-checkbox').addEventListener('change', () => toggleTodo(todo.id));
      li.querySelector('.delete-btn').addEventListener('click', () => deleteTodo(todo.id));

      todoList.appendChild(li);
    });
  }

  updateStats();
}

function updateStats() {
  const total = todos.length;
  const active = todos.filter((t) => !t.completed).length;
  const completed = todos.filter((t) => t.completed).length;

  document.getElementById('totalCount').textContent = total;
  document.getElementById('activeCount').textContent = active;
  document.getElementById('completedCount').textContent = completed;
}

// initial render
renderTodos();
