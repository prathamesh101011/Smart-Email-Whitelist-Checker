function onGmailMessageOpen(e) {

  var message = GmailApp.getMessageById(e.gmail.messageId);
  var body = message.getPlainBody();
  var userEmail = Session.getActiveUser().getEmail();

  var url = "https://karson-unparched-fallon.ngrok-free.dev/check";

  var options = {
    method: "post",
    contentType: "application/json",
    headers: {
      "x-api-key": "supersecretkey123"
    },
    payload: JSON.stringify({
      user_email: userEmail,
      email_text: body
    }),
    muteHttpExceptions: true
  };

  var response = UrlFetchApp.fetch(url, options);

  var result = JSON.parse(response.getContentText());

  var card = CardService.newCardBuilder()
    .setHeader(CardService.newCardHeader().setTitle("AI Spam Analyzer"))
    .addSection(
      CardService.newCardSection()
        .addWidget(
          CardService.newTextParagraph().setText(
            "Spam Probability: " + result.spam_probability +
            "<br>Final Score: " + result.final_score +
            "<br><b>Decision: " + result.prediction + "</b>"
          )
        )
    )
    .build();

  return [card];
}