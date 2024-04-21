/**
 * Abstract job validation class that mandates the validate function.
 * All job validators will implement this class.
 */

class GenericJobValidator {
    validate() {
        throw new Error("Method 'validated' must be implemented by subclass");
    }
}

export default GenericJobValidator;