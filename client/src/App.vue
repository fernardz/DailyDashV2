<template>
  <div id="app">
    <div id="nav">
      <router-link to="/dashboard">Dashboard</router-link> |
      <router-link to="/water">Water</router-link> |
      <router-link to="/vitamin">Vitamin</router-link> |
      <router-link to="/activity">Acitvity</router-link> |
      <router-link to="/task">Task</router-link>
    </div>
    <router-view/>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 0px;
}

#nav {
  padding: 10px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
