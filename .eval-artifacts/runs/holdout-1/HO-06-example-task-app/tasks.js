(function (root) {
  "use strict";

  function addTask(list, title) {
    var nextId = list.reduce(function (m, t) { return Math.max(m, t.id); }, 0) + 1;
    return list.concat([{ id: nextId, title: title, done: false }]);
  }

  function toggleDone(list, id) {
    return list.map(function (t) {
      return t.id === id ? { id: t.id, title: t.title, done: !t.done } : t;
    });
  }

  function clearCompleted(list) {
    return list.filter(function (t) { return t.done === false; });
  }

  function countCompleted(list) {
    return list.filter(function (t) { return t.done === true; }).length;
  }

  function handleClearCompleted(list, confirmFn) {
    var n = countCompleted(list);
    if (n === 0) return list;
    var ok = confirmFn("Remove " + n + " completed task(s)? This cannot be undone.");
    return ok === true ? clearCompleted(list) : list;
  }

  var api = {
    addTask: addTask,
    toggleDone: toggleDone,
    clearCompleted: clearCompleted,
    countCompleted: countCompleted,
    handleClearCompleted: handleClearCompleted
  };

  if (typeof module !== "undefined" && module.exports) module.exports = api;
  if (typeof window !== "undefined") window.Tasks = api;
})(this);
