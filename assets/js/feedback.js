import {
  __name
} from "../chunk-Y5CWL2B3.js";

// js/feedback.ts
var MAX_COMMENT_LENGTH = 2e3;
var lastFeedbackItemId = null;
var feedbackYes = document.getElementById("feedback-yes");
var feedbackNo = document.getElementById("feedback-no");
var feedbackForm = document.getElementById("feedback-form");
var feedbackSection = document.getElementById("feedback-section");
var feedbackComment = document.getElementById(
  "feedback-comment"
);
var feedbackCommentCount = document.getElementById("feedback-comment-count");
feedbackComment?.addEventListener("input", () => {
  const length = feedbackComment.value.length;
  if (feedbackCommentCount) {
    feedbackCommentCount.textContent = `${length} / ${MAX_COMMENT_LENGTH}`;
    const atLimit = length >= MAX_COMMENT_LENGTH;
    feedbackCommentCount.classList.toggle("text-red-600", atLimit);
    feedbackCommentCount.classList.toggle("dark:text-red-400", atLimit);
    feedbackCommentCount.classList.toggle("text-gray-600", !atLimit);
    feedbackCommentCount.classList.toggle("dark:text-gray-400", !atLimit);
  }
});
feedbackYes?.addEventListener("click", () => {
  sendFeedback({
    sentiment: "yes"
  });
});
feedbackNo?.addEventListener("click", () => {
  sendFeedback({
    sentiment: "no"
  });
});
feedbackForm?.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(feedbackForm);
  const form = Object.fromEntries(formData.entries());
  const ok = await sendFeedback({
    sentiment: form["feedback-vote"],
    comment: form["feedback-comment"],
    contact: form["feedback-contact"]
  });
  if (feedbackSection) {
    feedbackSection.innerHTML = ok ? "<p>Thank you for helping make the Deno docs awesome!</p>" : "<p>Sorry, something went wrong sending your feedback. Please try again later.</p>";
  }
});
var guideRequestForm = document.getElementById("guide-request-form");
var guideRequestBox = document.getElementById("guide-request-box");
guideRequestForm?.addEventListener("submit", (event) => {
  event.preventDefault();
  const formData = new FormData(guideRequestForm);
  const form = Object.fromEntries(formData.entries());
  const comment = form["guide-request-comment"]?.trim();
  if (!comment) return;
  sendFeedback({
    sentiment: "no",
    comment: `[Guide request] ${comment}`,
    contact: form["guide-request-contact"]
  });
  if (guideRequestBox) {
    guideRequestBox.innerHTML = "<p>Thanks! Your request has been filed \u2014 we'll take a look.</p>";
  }
});
async function sendFeedback(feedback) {
  feedback.path = feedback.path || new URL(window.location.href).pathname;
  feedback.id = lastFeedbackItemId ? lastFeedbackItemId : null;
  const result = await fetch("/_api/send-feedback", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(feedback)
  });
  const responseBody = await result.json();
  lastFeedbackItemId = responseBody.id;
  if (!result.ok) {
    console.error("Failed to send feedback", responseBody);
  }
  return result.ok;
}
__name(sendFeedback, "sendFeedback");
