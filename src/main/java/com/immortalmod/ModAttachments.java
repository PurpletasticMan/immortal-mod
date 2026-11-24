package com.immortalmod;

import com.mojang.serialization.Codec;
import net.fabricmc.fabric.api.attachment.v1.AttachmentRegistry;
import net.fabricmc.fabric.api.attachment.v1.AttachmentType;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.ai.attributes.AttributeInstance;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;

/** Stores how much extra max health (in half-hearts) a player has gained from heart items. Survives death. */
public final class ModAttachments {
	private static final Identifier MODIFIER_ID = ImmortalMod.id("bonus_hearts");

	public static final AttachmentType<Integer> BONUS_HEALTH = AttachmentRegistry.create(
			ImmortalMod.id("bonus_health"),
			builder -> builder.initializer(() -> 0).persistent(Codec.INT).copyOnDeath()
	);

	private ModAttachments() {
	}

	public static void init() {
		// touching the class registers the attachment
	}

	/** Adds half-hearts (2 = one heart) and applies them. */
	public static void addBonusHealth(ServerPlayer player, int halfHearts) {
		int total = player.getAttachedOrCreate(BONUS_HEALTH) + halfHearts;
		player.setAttached(BONUS_HEALTH, total);
		apply(player);
		player.heal(halfHearts);
	}

	/** Re-applies the stored bonus as a permanent max-health modifier. Safe to call any time. */
	public static void apply(ServerPlayer player) {
		AttributeInstance maxHealth = player.getAttribute(Attributes.MAX_HEALTH);
		if (maxHealth == null) {
			return;
		}
		maxHealth.removeModifier(MODIFIER_ID);
		int bonus = player.getAttachedOrCreate(BONUS_HEALTH);
		if (bonus > 0) {
			maxHealth.addPermanentModifier(new AttributeModifier(MODIFIER_ID, bonus, AttributeModifier.Operation.ADD_VALUE));
		}
	}
}
