function signatureMatch(input) {
  const signatures = ['malicious', 'trojan', 'worm', 'phishing'];
  for (const sig of signatures) {
    if (input.toLowerCase().includes(sig)) {
      return `signature match: ${sig}`;
    }
  }
  return null;
}

module.exports = { signatureMatch };