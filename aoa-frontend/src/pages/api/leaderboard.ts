import type { NextApiRequest, NextApiResponse } from 'next';
import { MongoClient } from 'mongodb';

const uri = process.env.MONGO_URI!;

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
    const { chatId } = req.query;
    if (!chatId || typeof chatId !== 'string') {
        return res.status(400).json({ error: 'chatId required' });
    }
    const client = new MongoClient(uri);
    try {
        await client.connect();
        const db = client.db(chatId);
        const collection = db.collection('prayge_tally');
        const leaderboard = await collection
            .find({})
            .sort({ count: -1 })
            .toArray();
        res.status(200).json(leaderboard);
    } catch (e) {
        res.status(500).json({ error: 'Failed to fetch leaderboard' });
    } finally {
        await client.close();
    }
}
