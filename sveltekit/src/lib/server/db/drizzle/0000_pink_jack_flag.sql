-- Current sql file was generated after introspecting the database
-- If you want to run this migration please uncomment this code before executing migrations
/*
CREATE TABLE `beer` (
	`id` integer PRIMARY KEY AUTOINCREMENT,
	`name` text NOT NULL,
	`style` text NOT NULL,
	`country_iso_3166_id` text NOT NULL,
	`abv` numeric NOT NULL,
	`volume_ml` integer NOT NULL,
	`price_kr` integer NOT NULL,
	`category_id` integer NOT NULL,
	`available` numeric NOT NULL,
	`last_moved` integer DEFAULT 0 NOT NULL,
	FOREIGN KEY (`category_id`) REFERENCES `beer_category`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE TABLE `beer_category` (
	`id` integer PRIMARY KEY AUTOINCREMENT,
	`name_sv` text NOT NULL,
	`name_en` text NOT NULL,
	`priority` integer NOT NULL
);
--> statement-breakpoint
CREATE TABLE `food` (
	`id` integer PRIMARY KEY AUTOINCREMENT,
	`name` text NOT NULL,
	`price_kr` integer NOT NULL,
	`available` numeric NOT NULL
);
--> statement-breakpoint
CREATE TABLE `snack` (
	`id` integer PRIMARY KEY AUTOINCREMENT,
	`name` text NOT NULL,
	`price_kr` integer NOT NULL,
	`available` numeric NOT NULL
);
--> statement-breakpoint
CREATE TABLE `worker` (
	`id` integer PRIMARY KEY AUTOINCREMENT,
	`display_name` text NOT NULL,
	`first_name` text NOT NULL,
	`last_name` text NOT NULL,
	`personal_id_number` text NOT NULL,
	`telephone` text,
	`email` text NOT NULL,
	`address` text,
	`note` text,
	`status_id` integer NOT NULL,
	FOREIGN KEY (`status_id`) REFERENCES `worker_status`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE TABLE `worker_status` (
	`id` integer PRIMARY KEY AUTOINCREMENT,
	`name` text NOT NULL
);
--> statement-breakpoint
CREATE TABLE `shift` (
	`id` integer PRIMARY KEY AUTOINCREMENT,
	`worker_id` integer NOT NULL,
	`shift_type_id` integer NOT NULL,
	`date` text NOT NULL,
	`start` text NOT NULL,
	`end` text NOT NULL,
	`created_at` numeric,
	FOREIGN KEY (`shift_type_id`) REFERENCES `shift_type`(`id`) ON UPDATE no action ON DELETE no action,
	FOREIGN KEY (`worker_id`) REFERENCES `worker`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE TABLE `shift_type` (
	`id` integer PRIMARY KEY AUTOINCREMENT,
	`name` text NOT NULL
);
--> statement-breakpoint
CREATE TABLE `opening_hours` (
	`id` integer PRIMARY KEY AUTOINCREMENT,
	`date` text NOT NULL,
	`start` text,
	`end` text
);
--> statement-breakpoint
CREATE TABLE `news` (
	`id` integer PRIMARY KEY AUTOINCREMENT,
	`time` text NOT NULL,
	`title_en` text NOT NULL,
	`body_en` text NOT NULL,
	`title_sv` text NOT NULL,
	`body_sv` text NOT NULL
);

*/