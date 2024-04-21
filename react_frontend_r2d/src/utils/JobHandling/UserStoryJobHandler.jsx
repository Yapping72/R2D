import GenericJobHandler from "./GenericJobHandlerUtility";
import UserStoryJobValidator from "../Validators/UserStoryJobValidator";
import UserStoryJobSanitizer from "../Sanitizers/UserStoryJobSanitizer";

/**
 * Concrete class for GenericJobHandlerUtility
 */
class UserStoryJobHandler extends GenericJobHandler {
    constructor(data) {
        super(new UserStoryJobValidator(data),new UserStoryJobSanitizer(data),  null); // Pass an instance of UserStoryJobValidator
        this.data = data; // Set the data property after calling super
    }
}

export default UserStoryJobHandler