/**
 * Constants related to validations.
 */

/**
 * The maximum number of words allowed in the 'feature' field of a user story.
 * This limit helps ensure concise feature descriptions and data consistency.
 */
export const MAX_USER_STORY_FEATURE_LENGTH = 15;

/**
 * The maximum number of words allowed in the 'sub feature' field of a user story.
 * This limit helps ensure concise sub-feature descriptions for UI display and database storage.
 */
export const MAX_USER_STORY_SUB_FEATURE_LENGTH = 15;

/**
 * The maximum number of words allowed in the 'requirement' field of a user story.
 * This limit helps ensure that requirement descriptions remain concise and manageable
 * within user interfaces and database entries.
 */
export const MAX_USER_STORY_REQUIREMENT_LENGTH = 300;

/**
 * The maximum number of words allowed in the 'acceptance criteria' field of a user story.
 * This limit helps ensure that acceptance criteria descriptions remain concise and manageable
 * within user interfaces and database entries.
 */
export const MAX_USER_STORY_ACCEPTANCE_CRITERIA_LENGTH = 300;

/**
 * The maximum number of words allowed in the 'additional information' field of a user story.
 * This limit helps ensure that additional information descriptions remain concise and manageable
 * within user interfaces and database entries.
 */
export const MAX_USER_STORY_ADDITIONAL_INFORMATION_LENGTH = 100;

/**
 * Limits the number of words in each service entry of a user story.
 * This limit helps ensure that service entries are concise and manageable.
 */
export const MAX_SERVICE_TO_USE_ENTRY_LENGTH = 10;

/**
 * Limits the number of services that a user story can define.
 * This limit helps ensure that the user story does not specify an excessive number of services.
 */
export const MAX_SERVICES_TO_USE = 15;

/**
 * The maximum number of words allowed in the ID field of a user story.
 * This limit helps ensure that user story IDs remain concise and manageable.
 */
export const MAX_USER_STORY_ID_LENGTH = 3;
