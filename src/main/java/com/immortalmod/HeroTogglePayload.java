package com.immortalmod;

import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;

/** Empty packet the client sends when the hero hotkey is pressed. */
public final class HeroTogglePayload implements CustomPacketPayload {
	public static final HeroTogglePayload INSTANCE = new HeroTogglePayload();
	public static final CustomPacketPayload.Type<HeroTogglePayload> TYPE = new CustomPacketPayload.Type<>(ImmortalMod.id("hero_toggle"));
	public static final StreamCodec<RegistryFriendlyByteBuf, HeroTogglePayload> CODEC = StreamCodec.unit(INSTANCE);

	private HeroTogglePayload() {
	}

	@Override
	public Type<? extends CustomPacketPayload> type() {
		return TYPE;
	}
}
