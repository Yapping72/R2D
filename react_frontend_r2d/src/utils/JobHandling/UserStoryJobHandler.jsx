import GenericJobHandler from "./GenericJobHandlerUtility";
import UserStoryJobValidator from "../Validators/UserStoryJobValidator";
import UserStoryJobSanitizer from "../Sanitizers/UserStoryJobSanitizer";

/**
 * UserStoryJobHandler, instantiates the validators, sanitizers and repository classes
 * 
 */
class UserStoryJobHandler extends GenericJobHandler {
    constructor(data) {
        super(new UserStoryJobValidator(data),new UserStoryJobSanitizer(data),  null); // Pass an instance of UserStoryJobValidator
    }
}

export default UserStoryJobHandler