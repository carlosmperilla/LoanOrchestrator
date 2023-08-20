export default eventHandler(async (event) => {
  const API_BASE = process.env.NUXT_API_BASE;
  const ForbiddenError = createError({
    statusCode: 403,
    statusMessage: "Forbidden Error",
  });
  const BadRequest = (message: string) => {
    return createError({
      statusCode: 400,
      statusMessage: "Bad Request",
      message,
    });
  };
  let loanrequestData;
  let applicantData;

  const body = await readBody(event);

  const applicantBody = {
    dni: body.dni,
    first_name: body.firstName,
    last_name: body.lastName,
    gender: body.gender,
    email: body.email,
  };
  const loanrequestBody = {
    amount: body.amount,
  };

  if (loanrequestBody.amount < 0) {
    let message = {
      amount: ["Asegúrese de que este valor es mayor o igual a 0.0."],
    };
    console.log(message);
    throw BadRequest(JSON.stringify(message));
  }

  try {
    applicantData = await $fetch("api/applicants/", {
      baseURL: API_BASE,
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        ...applicantBody,
      }),
    });
  } catch (error) {
    console.warn(error);
    console.warn((error as any).data);
    if ((error as any).statusCode === 400) {
      throw BadRequest(JSON.stringify((error as any).data));
    } else {
      throw ForbiddenError;
    }
  }

  const applicantUrl = (applicantData as any).url;

  try {
    loanrequestData = await $fetch("api/loanrequests/", {
      baseURL: API_BASE,
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        ...loanrequestBody,
        applicant: applicantUrl,
      }),
    });
  } catch (error) {
    console.warn(error);
    console.warn((error as any).data);
    if ((error as any).statusCode === 400) {
      throw BadRequest(JSON.stringify((error as any).data));
    } else {
      throw ForbiddenError;
    }
  }

  return {
    ...(loanrequestData as any),
    url: undefined,
    applicant: undefined,
  };
});
