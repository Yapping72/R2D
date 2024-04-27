import {GenericQueueRepository} from './GenericQueueRepository'

export class UserStoryJobQueueRepository extends GenericFileRepository {
    constructor() {
      super("r2d-user-story-db", "user-story-file-store");
    }
}