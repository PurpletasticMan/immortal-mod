package com.createshop;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.level.storage.LevelResource;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

/** The spot players go to with /shop. Set with /setshop, saved in <world>/createshop_warp.json */
public final class WarpManager {
	public record Warp(String dimId, double x, double y, double z, float yaw, float pitch) {}

	private static Warp warp;
	private static MinecraftServer loadedFor;
	private static Path file;

	private WarpManager() {}

	private static void ensureLoaded(MinecraftServer server) {
		if (loadedFor == server) return;
		loadedFor = server;
		warp = null;
		file = server.getWorldPath(LevelResource.ROOT).resolve("createshop_warp.json");
		if (!Files.exists(file)) return;
		try {
			JsonObject o = JsonParser.parseString(Files.readString(file)).getAsJsonObject();
			warp = new Warp(
					o.get("dim").getAsString(),
					o.get("x").getAsDouble(),
					o.get("y").getAsDouble(),
					o.get("z").getAsDouble(),
					o.get("yaw").getAsFloat(),
					o.get("pitch").getAsFloat());
		} catch (Exception e) {
			CreateShopMod.LOGGER.error("Could not read {}", file, e);
		}
	}

	public static Warp get(MinecraftServer server) {
		ensureLoaded(server);
		return warp;
	}

	public static void set(MinecraftServer server, Warp newWarp) {
		ensureLoaded(server);
		warp = newWarp;
		JsonObject o = new JsonObject();
		o.addProperty("dim", newWarp.dimId());
		o.addProperty("x", newWarp.x());
		o.addProperty("y", newWarp.y());
		o.addProperty("z", newWarp.z());
		o.addProperty("yaw", newWarp.yaw());
		o.addProperty("pitch", newWarp.pitch());
		try {
			Files.writeString(file, o.toString());
		} catch (IOException e) {
			CreateShopMod.LOGGER.error("Could not save {}", file, e);
		}
	}
}
