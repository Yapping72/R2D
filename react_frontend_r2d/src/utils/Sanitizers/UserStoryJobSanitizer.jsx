import GenericJobSanitizer from './GenericJobSanitizer'
import { MAX_USER_STORY_FEATURE_LENGTH, MAX_USER_STORY_SUB_FEATURE_LENGTH, MAX_USER_STORY_REQUIREMENT_LENGTH, MAX_USER_STORY_ACCEPTANCE_CRITERIA_LENGTH, MAX_USER_STORY_ADDITIONAL_INFORMATION_LENGTH, MAX_SERVICE_TO_USE_ENTRY_LENGTH, MAX_SERVICES_TO_USE, MAX_USER_STORY_ID_LENGTH } from "../Validators/ValidationConstants";

class UserStoryJobSanitizer extends GenericJobSanitizer {
    constructor(data) {
        super();
        this.data = data;
    }

    escapeHTML(input) {
        if (typeof input !== 'string') {
            return '';
        }

        return input.replace(/[&<>"']/g, function (match) {
            switch (match) {
                case '&':
                    return '&amp;';
                case '<':
                    return '&lt;';
                case '>':
                    return '&gt;';
                case '"':
                    return '&quot;';
                case "'":
                    return '&#x27;';
                default:
                    return match;
            }
        });
    }
    getSanitizedData(data) {
        console.debug("In UserStoryJobSanitizer")
        console.debug(data);
        return data;
    }
}

export default UserStoryJobSanitizer;