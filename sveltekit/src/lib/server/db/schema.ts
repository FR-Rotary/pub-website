import { sqliteTable, foreignKey, integer, text, numeric } from "drizzle-orm/sqlite-core"
import { sql } from "drizzle-orm"

export const beer = sqliteTable("beer", {
	id: integer().primaryKey({ autoIncrement: true }),
	name: text().notNull(),
	style: text().notNull(),
	countryIso3166Id: text("country_iso_3166_id").notNull(),
	abv: numeric().notNull(),
	volumeMl: integer("volume_ml").notNull(),
	priceKr: integer("price_kr").notNull(),
	categoryId: integer("category_id").notNull().references(() => beerCategory.id),
	available: numeric().notNull(),
	lastMoved: integer("last_moved").default(0).notNull(),
});

export const beerCategory = sqliteTable("beer_category", {
	id: integer().primaryKey({ autoIncrement: true }),
	nameSv: text("name_sv").notNull(),
	nameEn: text("name_en").notNull(),
	priority: integer().notNull(),
});

export const food = sqliteTable("food", {
	id: integer().primaryKey({ autoIncrement: true }),
	name: text().notNull(),
	priceKr: integer("price_kr").notNull(),
	available: numeric().notNull(),
});

export const snack = sqliteTable("snack", {
	id: integer().primaryKey({ autoIncrement: true }),
	name: text().notNull(),
	priceKr: integer("price_kr").notNull(),
	available: numeric().notNull(),
});

export const worker = sqliteTable("worker", {
	id: integer().primaryKey({ autoIncrement: true }),
	displayName: text("display_name").notNull(),
	firstName: text("first_name").notNull(),
	lastName: text("last_name").notNull(),
	personalIdNumber: text("personal_id_number").notNull(),
	telephone: text(),
	email: text().notNull(),
	address: text(),
	note: text(),
	statusId: integer("status_id").notNull().references(() => workerStatus.id),
});

export const workerStatus = sqliteTable("worker_status", {
	id: integer().primaryKey({ autoIncrement: true }),
	name: text().notNull(),
});

export const shift = sqliteTable("shift", {
	id: integer().primaryKey({ autoIncrement: true }),
	workerId: integer("worker_id").notNull().references(() => worker.id),
	shiftTypeId: integer("shift_type_id").notNull().references(() => shiftType.id),
	date: text().notNull(),
	start: text().notNull(),
	end: text().notNull(),
	createdAt: numeric("created_at"),
});

export const shiftType = sqliteTable("shift_type", {
	id: integer().primaryKey({ autoIncrement: true }),
	name: text().notNull(),
});

export const openingHours = sqliteTable("opening_hours", {
	id: integer().primaryKey({ autoIncrement: true }),
	date: text().notNull(),
	start: text(),
	end: text(),
});

export const news = sqliteTable("news", {
	id: integer().primaryKey({ autoIncrement: true }),
	time: text().notNull(),
	titleEn: text("title_en").notNull(),
	bodyEn: text("body_en").notNull(),
	titleSv: text("title_sv").notNull(),
	bodySv: text("body_sv").notNull(),
});

