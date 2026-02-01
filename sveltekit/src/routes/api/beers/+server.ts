import { db } from "$lib/server/db/db"
import { beer } from "$lib/server/db/schema"
import { json } from "@sveltejs/kit"
import { eq } from "drizzle-orm"

export async function GET() {
	const beers = await db.select({
		name: beer.name,
		style: beer.style,
		countyISO: beer.countryIso3166Id,
		abv: beer.abv,
		vol_ml: beer.volumeMl,
		price_kr: beer.priceKr,
	}).
		from(beer).
		where(eq(beer.available, "1"))
	return json(beers)
}
