import { relations } from "drizzle-orm/relations";
import { beerCategory, beer, workerStatus, worker, shiftType, shift } from "./schema";

export const beerRelations = relations(beer, ({one}) => ({
	beerCategory: one(beerCategory, {
		fields: [beer.categoryId],
		references: [beerCategory.id]
	}),
}));

export const beerCategoryRelations = relations(beerCategory, ({many}) => ({
	beers: many(beer),
}));

export const workerRelations = relations(worker, ({one, many}) => ({
	workerStatus: one(workerStatus, {
		fields: [worker.statusId],
		references: [workerStatus.id]
	}),
	shifts: many(shift),
}));

export const workerStatusRelations = relations(workerStatus, ({many}) => ({
	workers: many(worker),
}));

export const shiftRelations = relations(shift, ({one}) => ({
	shiftType: one(shiftType, {
		fields: [shift.shiftTypeId],
		references: [shiftType.id]
	}),
	worker: one(worker, {
		fields: [shift.workerId],
		references: [worker.id]
	}),
}));

export const shiftTypeRelations = relations(shiftType, ({many}) => ({
	shifts: many(shift),
}));