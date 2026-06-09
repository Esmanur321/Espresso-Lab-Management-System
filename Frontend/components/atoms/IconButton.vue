<template>
  <button class="icon-button">
    <slot>
      <span class="icon-placeholder">👤</span>
    </slot>
  </button>
</template>

<style scoped>
.icon-button {
  background-color: #db2c2c;
  color: white;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.icon-button:hover {
  background-color: #c00a00;
}
.icon-placeholder {
  font-size: 1.2rem;
}
</style>