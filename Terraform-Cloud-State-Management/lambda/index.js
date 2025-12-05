exports.handler = async (event) => {
  console.log("Event Received:", JSON.stringify(event));

  return {
    statusCode: 200,
    body: JSON.stringify({
      message: "Lambda invoked successfully!",
      input: event,
    }),
  };
};
