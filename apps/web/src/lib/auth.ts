"use client";

import { createClient, type SupabaseClient, type User } from "@supabase/supabase-js";
import { create } from "zustand";
import { exportProgress, initialProgress, useProgress, type ProgressData } from "./progress";

const URL = process.env.NEXT_PUBLIC_SUPABASE_URL;
const ANON_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

/** Accounts are optional: without these env vars the app stays in guest (local-only) mode. */
export const authEnabled = Boolean(URL && ANON_KEY);

let client: SupabaseClient | null = null;
function supabase(): SupabaseClient {
  if (!URL || !ANON_KEY) throw new Error("auth is not configured");
  client ??= createClient(URL, ANON_KEY, { auth: { detectSessionInUrl: true, persistSession: true } });
  return client;
}

export type SyncState = "idle" | "syncing" | "synced" | "error";

interface AuthStore {
  user: User | null;
  ready: boolean;
  sync: SyncState;
  init(): void;
  signInWithGoogle(): Promise<string | null>;
  signInWithEmail(email: string, password: string): Promise<string | null>;
  signUpWithEmail(email: string, password: string): Promise<"confirm" | string | null>;
  signOut(): Promise<void>;
  syncNow(): Promise<void>;
}

const basePath = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
const redirectUrl = () => `${window.location.origin}${basePath}/`;

function progressData(): ProgressData {
  return JSON.parse(exportProgress()).data as ProgressData;
}

/** Remote wins only if it has strictly more XP; progress only grows, so more XP means newer. */
function pickWinner(local: ProgressData, remote: ProgressData | null): "local" | "remote" {
  if (!remote || remote.version !== 1) return "local";
  return remote.xp > local.xp ? "remote" : "local";
}

let initialised = false;
let pushTimer: ReturnType<typeof setTimeout> | undefined;
let applyingRemote = false;

async function push(userId: string) {
  const { error } = await supabase()
    .from("progress")
    .upsert({ user_id: userId, data: progressData(), updated_at: new Date().toISOString() });
  if (error) throw error;
}

export const useAuth = create<AuthStore>()((set, get) => ({
  user: null,
  ready: !authEnabled,
  sync: "idle",

  init() {
    if (!authEnabled || initialised) return;
    initialised = true;
    const sb = supabase();
    void sb.auth.getSession().then(({ data }) => {
      set({ user: data.session?.user ?? null, ready: true });
      if (data.session?.user) void get().syncNow();
    });
    sb.auth.onAuthStateChange((event, session) => {
      set({ user: session?.user ?? null, ready: true });
      if (event === "SIGNED_IN" && session?.user) void get().syncNow();
      if (event === "SIGNED_OUT") set({ sync: "idle" });
    });
    // Debounced upload after every local change while signed in.
    useProgress.subscribe(() => {
      const { user } = get();
      if (!user || applyingRemote) return;
      clearTimeout(pushTimer);
      pushTimer = setTimeout(() => {
        set({ sync: "syncing" });
        push(user.id).then(
          () => set({ sync: "synced" }),
          () => set({ sync: "error" }),
        );
      }, 1500);
    });
  },

  async signInWithGoogle() {
    const { error } = await supabase().auth.signInWithOAuth({
      provider: "google",
      options: { redirectTo: redirectUrl() },
    });
    return error?.message ?? null;
  },

  async signInWithEmail(email, password) {
    const { error } = await supabase().auth.signInWithPassword({ email, password });
    return error?.message ?? null;
  },

  async signUpWithEmail(email, password) {
    const { data, error } = await supabase().auth.signUp({
      email,
      password,
      options: { emailRedirectTo: redirectUrl() },
    });
    if (error) return error.message;
    return data.session ? null : "confirm";
  },

  async signOut() {
    clearTimeout(pushTimer);
    await supabase().auth.signOut();
    set({ user: null, sync: "idle" });
  },

  async syncNow() {
    const { user } = get();
    if (!user) return;
    set({ sync: "syncing" });
    try {
      const { data, error } = await supabase().from("progress").select("data").eq("user_id", user.id).maybeSingle();
      if (error) throw error;
      const local = progressData();
      const remote = (data?.data ?? null) as ProgressData | null;
      if (pickWinner(local, remote) === "remote" && remote) {
        applyingRemote = true;
        try {
          useProgress.getState().importData({ ...initialProgress(), ...remote });
        } finally {
          applyingRemote = false;
        }
      } else {
        await push(user.id);
      }
      set({ sync: "synced" });
    } catch {
      set({ sync: "error" });
    }
  },
}));
