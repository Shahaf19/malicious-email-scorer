const VERDICT_STYLES = {
  // Deliberately not "Safe": finding no evidence is not proof that an email is harmless.
  safe: {
    label: '✅ No warning signs found',
    advice: 'Not a guarantee: stay careful with unexpected requests for money or passwords.',
  },
  suspicious: {
    label: '⚠️ Suspicious',
    advice:
      "Don't click links or open attachments until you confirm the sender another way (e.g. call them).",
  },
  malicious: {
    label: '⛔ Malicious',
    advice:
      "Don't click links, open attachments or reply. Report it: Gmail's ⋮ menu → \"Report phishing\".",
  },
};

function buildResultCard(result) {
  const style = VERDICT_STYLES[result.verdict];
  const adviceSection = CardService.newCardSection()
    .setHeader('What to do')
    .addWidget(CardService.newTextParagraph().setText(style.advice));

  return newAddonCard()
    .addSection(buildVerdictSection(result, style))
    .addSection(adviceSection)
    .build();
}

function buildVerdictSection(result, style) {
  return CardService.newCardSection().addWidget(
    CardService.newDecoratedText()
      .setTopLabel('Verdict')
      .setText('<b>' + style.label + '</b>')
      .setBottomLabel(scoreBar(result.score) + '  ' + result.score + ' / ' + MAX_SCORE)
  );
}

function scoreBar(score) {
  const filled = Math.round((score / MAX_SCORE) * SCORE_BAR_SEGMENTS);
  return '█'.repeat(filled) + '░'.repeat(SCORE_BAR_SEGMENTS - filled);
}

function buildErrorCard() {
  const message =
    "⚠️ <b>Couldn't analyze this email.</b><br>This is not a verdict: treat it with your usual caution.";
  return newAddonCard()
    .addSection(CardService.newCardSection().addWidget(CardService.newTextParagraph().setText(message)))
    .build();
}

function newAddonCard() {
  return CardService.newCardBuilder().setHeader(CardService.newCardHeader().setTitle(ADDON_TITLE));
}
