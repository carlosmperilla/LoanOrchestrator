<script setup>
import { ref, reactive } from "vue";

const errorMessages = {
  dni: "DNI",
  firstName: "Nombre",
  lastName: "Apellido",
  gender: "Género",
  email: "Email",
  amount: "Monto solicitado",
};

const form = reactive({
  dni: "",
  firstName: "",
  lastName: "",
  gender: "M",
  email: "",
  amount: 0,
  errors: {},
});

const result = ref(null);

async function checkLoan() {
  let data;
  let errors;
  try {
    const response = await fetch("/api/loanrequest", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(form),
    });
    data = await response.json();
    if (data.message !== undefined) {
      errors = JSON.parse(data.message);
      console.log(errors);
      form.errors = JSON.parse(data.message);
    } else {
      console.log("Success");
      result.value = data;
      form.errors = {};
    }
  } catch (error) {
    console.error(error);
  }
}
</script>

<template>
  <section class="form-container">
    <div v-if="Object.keys(form.errors).length > 0" class="errors">
      <p>Errores:</p>
      <ul>
        <li v-for="(error, key) in form.errors" :key="key">
          {{ errorMessages[key] }}: {{ error.join(", ") }}
        </li>
      </ul>
    </div>

    <div v-if="result" class="results">
      <p v-if="result.approved">Préstamo aprobado</p>
      <p v-else>Préstamo rechazado</p>
    </div>

    <form @submit.prevent="checkLoan" class="form">
      <label>DNI:</label>
      <input v-model="form.dni" type="text" required />
      <label>Nombre:</label>
      <input v-model="form.firstName" type="text" required />
      <label>Apellido:</label>
      <input v-model="form.lastName" type="text" required />
      <label>Género:</label>
      <select v-model="form.gender">
        <option value="M">Masculino</option>
        <option value="F">Femenino</option>
        <option value="O">Otro</option>
      </select>
      <label>Email:</label>
      <input v-model="form.email" type="email" required />
      <label>Monto solicitado:</label>
      <input v-model.number="form.amount" type="number" required />
      <button>Enviar</button>
    </form>
  </section>
</template>

<style lang="css">
.form-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  flex-direction: column;
  gap: 20px;
}

.form {
  background-color: #f4f4f4;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
  width: 500px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.form label {
  display: block;
  margin-bottom: 5px;
  align-self: flex-start;
  padding-left: 1em;
  font-weight: bold;
}

.form label:not(:first-child) {
  margin-top: 10px;
}

.form input[type="text"],
.form input[type="email"],
.form input[type="number"],
.form select {
  display: block;
  width: 80%;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
  border: none;
}

.form button {
  background-color: #333;
  color: #fff;
  padding: 10px 20px;
  border-radius: 5px;
  border: none;
}

.form button:active {
  transform: scale(0.97, 1);
  filter: opacity(0.9);
}

.errors {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
  padding: 10px;
}

.results {
  background-color: #f1f8d7;
  color: #67721c;
  border: 1px solid #d2ba07;
  border-radius: 4px;
  padding: 10px;
}

.results p,
.errors p {
  margin: 0;
}

.errors ul {
  margin: 0;
  padding-left: 20px;
}

@media (max-width: 600px) {
  .form {
    width: calc(100% - 40px);
    margin: auto;
    margin-top: -50px;
    max-width: none;
    box-shadow: none;
    border-radius: none;
    padding-top: calc(50px + env(safe-area-inset-top));
    padding-bottom: calc(20px + env(safe-area-inset-bottom));
    padding-left: calc(20px + env(safe-area-inset-left));
    padding-right: calc(20px + env(safe-area-inset-right));
    box-sizing: border-box;
    height: auto !important;
    min-height: calc(
      100% - env(safe-area-inset-top) - env(safe-area-inset-bottom)
    );
    position: relative;
    background-color: #fff;
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
    overscroll-behavior-y: contain;
  }
  .form input,
  select {
    background-color: lightgray;
  }
}
</style>
