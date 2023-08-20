export default eventHandler(async (event) => {
  const API_BASE = process.env.NUXT_API_BASE;
  const slug = (event.context.params as any).slug;

  const headers = event.node.req.headers;

  let applicantData;
  try {
    applicantData = await $fetch(`api/applicants/${slug}`, {
      baseURL: API_BASE,
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: headers.authorization || "",
      },
    });
  } catch (error) {
    console.warn(error);
    console.warn((error as any).data);
  }

  return {};
});
