import GenericJobSanitizer from './GenericJobSanitizer'

class UserStoryJobSanitizer extends GenericJobSanitizer {
    constructor(data) {
        super();
        this.data = data;
    }

    getSanitizedData(data) {;
        return data;
    }
}
export default UserStoryJobSanitizer;