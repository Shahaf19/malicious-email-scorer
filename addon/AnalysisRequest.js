/**
 * Builds the POST /analyze body: the facts the backend analyzes, nothing else.
 * @param {GmailApp.GmailMessage} message
 * @return {Object}
 */
function buildAnalysisRequest(message) {
  return {
    headers: extractHeaderBlock(message.getRawContent()),
    subject: message.getSubject(),
    body_text: message.getPlainBody(),
    body_html: message.getBody(),
  };
}

/** The raw message is headers, a blank line, then the body; we keep only the headers. */
function extractHeaderBlock(rawContent) {
  const blankLineIndex = rawContent.search(/\r?\n\r?\n/);
  return blankLineIndex === -1 ? rawContent : rawContent.slice(0, blankLineIndex);
}
