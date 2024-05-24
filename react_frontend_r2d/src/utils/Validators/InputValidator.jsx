class InputValidator {
    /**
    * Validates the given email address.
    * @param {string} email - The email address to validate.
    * @returns {boolean} - Returns true if the email is valid, false otherwise.
    */
    static isValidEmail(email) {
        // Regular expression for validating an Email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    /**
        * Validates the given username.
        * @param {string} username - The username to validate.
        * @returns {boolean} - Returns true if the username is alphanumeric and between 9 and 64 characters with at least one digit.
        */
    static isValidUsername(username) {
        // Updated regex to check for at least one digit
        const usernameRegex = /^(?=.*\d)[a-zA-Z0-9]{9,64}$/;
        return usernameRegex.test(username);
    }
    /**
     * Validates the given display name.
     * @param {string} displayname - The display name to validate.
     * @returns {boolean} - Returns true if the display name contains only letters and is between 1 and 64 characters.
     */
    static isValidDisplayname(displayname) {
        const displaynameRegex = /^[a-zA-Z0-9 !@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]{1,64}$/;
        return displaynameRegex.test(displayname);
    }
    /**
     * Validates the given password.
     * @param {string} password - The password to validate.
     * @returns {boolean} - Returns true if the password is between 12 and 128 characters.
     */
    static isValidPassword(password) {
        return password.length >= 12 && password.length <= 128;
    }
    /**
     * Checks if the given password and confirmPassword match.
     * @param {string} password - The password.
     * @param {string} confirmPassword - The confirmation password.
     * @returns {boolean} - Returns true if the passwords match, false otherwise.
     */
    static doPasswordsMatch(password, confirmPassword) {
        return password === confirmPassword;
    }
    /**
     * Checks if the given value is non-empty.
     * @param {string} value - The value to check.
     * @returns {boolean} - Returns true if the value is non-empty, false otherwise.
     */
    static isNonEmpty(value) {
        return value && value.trim().length > 0;
    }
}

export default InputValidator;