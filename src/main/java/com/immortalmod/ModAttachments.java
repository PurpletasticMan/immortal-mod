package com.immortalmod;

import com.mojang.serialization.Codec;
import net.fabricmc.fabric.api.attachment.v1.AttachmentRegistry;
import net.fabricmc.fabric.api.attachment.v1.AttachmentSyncPredicate;
import net.fabricmc.fabric.api.attachment.v1.AttachmentType;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.resources.Identifier;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.ai.attributes.AttributeInstance;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;

/** How many extra hearts each kind of heart item has given a player. Survives death and is synced to the client for the HUD. */
public final class ModAttachments {
	private static final Identifier MODIFIER_ID = ImmortalMod.id("bonus_hearts");

	public static final AttachmentType<Integer> NORMAL_HEARTS = hearts("normal_hearts");
	public static final AttachmentType<Integer> IMMORTAL_HEARTS = hearts("immortal_hearts");
	public static final AttachmentType<Integer> GODLY_HEARTS = hearts("godly_hearts");

	private ModAttachments() {
	}

	private static AttachmentType<Integer> hearts(String name) {
		return AttachmentRegistry.create(
				ImmortalMod.id(name),
				builder -> builder.initializer(() -> 0)
						.persistent(Codec.INT)
						.copyOnDeath()
						.syncWith(ByteBufCodecs.INT, AttachmentSyncPredicate.targetOnly())
		);
	}

	public static void init() {
		// touching the class registers the attachments
	}

	public static void addHearts(ServerPlayer player, AttachmentType<Integer> kind, int hearts) {
		player.setAttached(kind, player.getAttachedOrCreate(kind) + hearts);
		apply(player);
		player.heal(hearts * 2.0F);
	}

	/** Re-applies all stored hearts as one permanent max-health modifier. Safe to call any time. */
	public static void apply(ServerPlayer player) {
		AttributeInstance maxHealth = player.getAttribute(Attributes.MAX_HEALTH);
		if (maxHealth == null) {
			return;
		}
		maxHealth.removeModifier(MODIFIER_ID);
		int halfHearts = 2 * (player.getAttachedOrCreate(NORMAL_HEARTS) + player.getAttachedOrCreate(IMMORTAL_HEARTS) + player.getAttachedOrCreate(GODLY_HEARTS));
		if (halfHearts > 0) {
			maxHealth.addPermanentModifier(new AttributeModifier(MODIFIER_ID, halfHearts, AttributeModifier.Operation.ADD_VALUE));
		}
	}
}
