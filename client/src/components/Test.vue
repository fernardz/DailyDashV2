<template>
  <div class="container">
      <div class="row">
          <div class="col-sm-10">
              <h1> Activities </h1>
              <hr><br><br>
              <tools></tools>
              <alert :message=message v-if="showMessage"></alert>
              <br><br>
              <div>{{ getCurrentDate() }}</div>
                <h3>Activity Count: {{current.sum}}</h3>
              <br><br>
              <table class="table table-hover">
                <thead>
                    <tr>
                        <th scope="col">Date</th>
                        <th scope="col">Minuites</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(water, index) in waters" :key="index">
                        <td>{{water.date}}</td>
                        <td>{{water.size}}</td>
                    </tr>

                </tbody>
              </table>
            </div>
      </div>
  </div>
</template>