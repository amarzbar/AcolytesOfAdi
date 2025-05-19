# AdiPray Leaderboard Frontend

This is a modern Next.js (TypeScript) web app for displaying the AdiPray leaderboard, powered by MongoDB and styled with Tailwind CSS.

## Features

- Displays a leaderboard of users who sent "prayge" emotes, with their Discord avatar, display name, username, and count.
- Connects to your MongoDB backend (same as your bot).
- Responsive, beautiful UI using Tailwind CSS.
- Fetches Discord avatars using user_id and Discord CDN.

## Getting Started

1. **Install dependencies:**

   ```sh
   npm install
   ```

2. **Set up your environment:**

   - Create a `.env.local` file in the project root with:

     ```
     MONGO_URI=mongodb://localhost:27017/
     ```

3. **Run the development server:**

   ```sh
   npm run dev
   ```

   Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

- `src/app/` - Main Next.js app directory
- `src/pages/api/leaderboard.ts` - API route to fetch leaderboard data from MongoDB
- `src/components/` - React components (to be created)
- `tailwind.config.js` - Tailwind CSS configuration

## Customization

- Update the MongoDB query logic in the API route as needed to match your bot's data structure.
- Extend the UI for more features or custom branding.

---

Made with ❤️ for AdiPray.
