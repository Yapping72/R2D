// constants.js

/**
 * Constants related to validations.
 */

/**
 * The maximum length of the 'feature' field in a user story.
 * This is used to validate input lengths to ensure data consistency
 * and meet database or display constraints.
 */
export const MAX_USER_STORY_FEATURE_LENGTH = 15;

/**
 * The maximum length of the 'sub feature' field in a user story.
 * This limit helps in maintaining concise sub feature descriptions
 * and ensures they are suitable for UI display and database storage.
 */
export const MAX_USER_STORY_SUB_FEATURE_LENGTH = 15;

/**
 * The maximum length of the 'requirement' field in a user story.
 * This cap on characters helps ensure that requirement descriptions
 * remain concise and manageable within user interfaces and database entries.
 */
export const MAX_USER_STORY_REQUIREMENT_LENGTH = 300;
