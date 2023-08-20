export default eventHandler(async (event) => {
  const API_BASE = process.env.NUXT_API_BASE;

  const headers = event.node.req.headers;

  interface Applicant {
    url: string;
    dni: string;
    first_name: string;
    last_name: string;
    gender: string;
    email: string;
    loanrequests: LoanRequest[];
  }

  interface LoanRequest {
    url: string;
    amount: number;
    approved: boolean;
  }

  interface Result {
    applicantId: string;
    loanId: string;
    dni: string;
    firstName: string;
    lastName: string;
    gender: string;
    email: string;
    amount: number;
    approved: boolean;
  }

  let applicantData;
  try {
    applicantData = await $fetch("api/applicants/", {
      baseURL: API_BASE,
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: headers.authorization || "",
      },
    });
  } catch (error) {
    console.warn(error);
    console.warn((error as any).data);
  }

  const applicants: Applicant[] = (applicantData as any).results;

  const results: Result[] = applicants.map((applicant) => {
    const { url, dni, first_name, last_name, gender, email, loanrequests } =
      applicant;

    function getUUID(url: string) {
      const regex =
        /\/([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})\//;
      let uuid = "";
      const match = url.match(regex);
      if (match) {
        uuid = match[1];
      }
      return uuid;
    }

    const applicantId = getUUID(url);

    const loanrequest = loanrequests[0];

    const loanId = getUUID(loanrequest?.url || "");

    const { amount, approved } = loanrequest || { amount: "", approved: "" };

    return {
      applicantId,
      loanId,
      dni,
      firstName: first_name,
      lastName: last_name,
      gender,
      email,
      amount,
      approved,
    };
  });

  return results;
});
