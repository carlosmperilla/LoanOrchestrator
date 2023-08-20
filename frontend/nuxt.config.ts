// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: false },
  pages: true, // Para la configuración de las paginas.
  // modules: ["@sidebase/nuxt-auth"],
  app: {
    head: {
      title: "Frontend Loan Request - Peticiones de prestamo",
      htmlAttrs: {
        lang: "es",
      },
      meta: [
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        {
          hid: "description",
          name: "description",
          content: "Frontend Loan Request - Peticiones de prestamo",
        },
        { name: "format-detection", content: "telephone=no" },
      ],
      link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
    },
    pageTransition: { name: "page", mode: "out-in" },
  },
  routeRules: {
    "/api/**": { cors: true },
  },
});
