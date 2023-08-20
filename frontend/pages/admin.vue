<script setup>
import { ref, onMounted } from "vue";

const loans = ref([]);

onMounted(async () => {
  const response = await fetch("/api/loanrequest", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("jwt") || ""}`,
    },
  });
  loans.value = await response.json();
});

async function editLoan(loan) {}

async function deleteLoan(applicantId) {
  console.log("eliminando");
  const response = await fetch(`/api/loanrequest/${applicantId}`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("jwt") || ""}`,
    },
  });
  const data = await response.json();
  console.log(data);
  const responsetwo = await fetch("/api/loanrequest", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("jwt") || ""}`,
    },
  });
  loans.value = await responsetwo.json();
}

const token = ref("");

async function saveToken() {
  localStorage.setItem("jwt", token.value);
  const response = await fetch("/api/loanrequest", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("jwt") || ""}`,
    },
  });
  loans.value = await response.json();
}

async function deleteToken() {
  localStorage.removeItem("jwt");
  token.value = null;
  loans.value = null;
}
</script>

<template>
  <div>
    <label for="token">Token JWT:</label>
    <input id="token" v-model="token" type="text" />
    <button @click="saveToken">Guardar</button>
    <button @click="deleteToken">Eliminar</button>
  </div>
  <section>
    <table>
      <thead>
        <tr>
          <th>DNI</th>
          <th>Nombre</th>
          <th>Apellido</th>
          <th>Género</th>
          <th>Email</th>
          <th>Monto solicitado</th>
          <th>Aprobado</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="loan in loans" :key="loan.loanId">
          <td>{{ loan.dni }}</td>
          <td>{{ loan.firstName }}</td>
          <td>{{ loan.lastName }}</td>
          <td>{{ loan.gender }}</td>
          <td>{{ loan.email }}</td>
          <td>{{ loan.amount }}</td>
          <td>{{ loan.approved ? "Sí" : "No" }}</td>
          <td>
            <button @click="editLoan(loan)">Editar</button>
            <button @click="deleteLoan(loan.applicantId)">Eliminar</button>
          </td>
        </tr>
      </tbody>
    </table>
  </section>
</template>
