package com.immortalmod;

import java.util.HashSet;
import java.util.Set;
import java.util.UUID;
import net.fabricmc.fabric.api.entity.event.v1.ServerLivingEntityEvents;
import net.fabricmc.fabric.api.entity.event.v1.ServerPlayerEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.fabricmc.fabric.api.event.player.AttackBlockCallback;
import net.fabricmc.fabric.api.networking.v1.ServerPlayConnectionEvents;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;

public final class ModEvents {
	/** Players we gave flight to (so we only take it back from players we gave it to). */
	private static final Set<UUID> FLYERS = new HashSet<>();

	private static final Set<Item> BEDROCK_BREAKERS = Set.of(ModItems.BEDROCK_PICKAXE, ModItems.IMMORTAL_PICKAXE, ModItems.GODLY_PICKAXE);

	private ModEvents() {
	}

	public static void init() {
		registerHearts();
		registerBedrockBreaking();
		registerTotems();
		registerArmourSets();
	}

	// ------------------------------------------------------------ hearts persist

	private static void registerHearts() {
		ServerPlayConnectionEvents.JOIN.register((handler, sender, server) -> ModAttachments.apply(handler.getPlayer()));
		ServerPlayerEvents.AFTER_RESPAWN.register((oldPlayer, newPlayer, alive) -> {
			ModAttachments.apply(newPlayer);
			newPlayer.setHealth(newPlayer.getMaxHealth());
		});
		ServerPlayerEvents.LEAVE.register(player -> FLYERS.remove(player.getUUID()));
	}

	// ------------------------------------------------------------ bedrock pickaxe

	private static void registerBedrockBreaking() {
		AttackBlockCallback.EVENT.register((player, level, hand, pos, direction) -> {
			if (player.isSpectator() || !BEDROCK_BREAKERS.contains(player.getItemInHand(hand).getItem())) {
				return InteractionResult.PASS;
			}
			BlockState state = level.getBlockState(pos);
			Block block = state.getBlock();
			boolean breakable = block == Blocks.BEDROCK || block == Blocks.REINFORCED_DEEPSLATE || block == Blocks.END_PORTAL_FRAME;
			if (!breakable) {
				return InteractionResult.PASS;
			}
			if (level instanceof ServerLevel serverLevel) {
				level.destroyBlock(pos, false, player);
				if (!player.isCreative()) {
					Block.popResource(serverLevel, pos, new ItemStack(block.asItem()));
				}
			}
			return InteractionResult.SUCCESS;
		});
	}

	// ------------------------------------------------------------ totems

	private static void registerTotems() {
		ServerLivingEntityEvents.ALLOW_DEATH.register((entity, source, amount) -> {
			if (!(entity instanceof ServerPlayer player) || source.is(DamageTypeTags.BYPASSES_INVULNERABILITY)) {
				return true;
			}
			boolean godly = hasInInventory(player, ModItems.GODLY_TOTEM);
			boolean immortal = hasInInventory(player, ModItems.IMMORTAL_TOTEM);
			if (!godly && !immortal) {
				return true;
			}
			player.setHealth(godly ? player.getMaxHealth() : Math.max(1.0F, player.getMaxHealth() * 0.5F));
			player.removeAllEffects();
			player.addEffect(new MobEffectInstance(MobEffects.REGENERATION, godly ? 20 * 45 : 20 * 20, godly ? 3 : 1));
			player.addEffect(new MobEffectInstance(MobEffects.ABSORPTION, 20 * 30, godly ? 9 : 4));
			player.addEffect(new MobEffectInstance(MobEffects.FIRE_RESISTANCE, 20 * 40, 0));
			player.addEffect(new MobEffectInstance(MobEffects.RESISTANCE, 20 * 10, godly ? 4 : 2));
			ServerLevel level = (ServerLevel) player.level();
			level.broadcastEntityEvent(player, (byte) 35); // vanilla totem pop animation
			level.playSound(null, player.getX(), player.getY(), player.getZ(), SoundEvents.TOTEM_USE, SoundSource.PLAYERS, 1.0F, 1.0F);
			return false; // cancel the death; the totem is NOT consumed
		});
	}

	private static boolean hasInInventory(ServerPlayer player, Item item) {
		Inventory inv = player.getInventory();
		for (int i = 0; i < inv.getContainerSize(); i++) {
			if (inv.getItem(i).is(item)) {
				return true;
			}
		}
		return false;
	}

	// ------------------------------------------------------------ armour sets

	private static void registerArmourSets() {
		// godly armour: no fall damage
		ServerLivingEntityEvents.ALLOW_DAMAGE.register((entity, source, amount) -> {
			if (entity instanceof ServerPlayer player && source.is(DamageTypeTags.IS_FALL) && wearing(player, ModItems.GODLY_HELMET, ModItems.GODLY_CHESTPLATE, ModItems.GODLY_LEGGINGS, ModItems.GODLY_BOOTS)) {
				return false;
			}
			return true;
		});

		ServerTickEvents.END_SERVER_TICK.register(server -> {
			boolean refresh = server.getTickCount() % 10 == 0;
			for (ServerPlayer player : server.getPlayerList().getPlayers()) {
				boolean godly = wearing(player, ModItems.GODLY_HELMET, ModItems.GODLY_CHESTPLATE, ModItems.GODLY_LEGGINGS, ModItems.GODLY_BOOTS);
				updateFlight(player, godly);
				if (!refresh) {
					continue;
				}
				if (godly) {
					effect(player, MobEffects.RESISTANCE, 3);
					effect(player, MobEffects.STRENGTH, 2);
					effect(player, MobEffects.SPEED, 1);
					effect(player, MobEffects.HASTE, 2);
					effect(player, MobEffects.REGENERATION, 2);
					effect(player, MobEffects.JUMP_BOOST, 1);
					effect(player, MobEffects.SATURATION, 0);
					effect(player, MobEffects.FIRE_RESISTANCE, 0);
					effect(player, MobEffects.WATER_BREATHING, 0);
					effect(player, MobEffects.NIGHT_VISION, 0, 260);
				} else if (wearing(player, ModItems.IMMORTAL_HELMET, ModItems.IMMORTAL_CHESTPLATE, ModItems.IMMORTAL_LEGGINGS, ModItems.IMMORTAL_BOOTS)) {
					effect(player, MobEffects.RESISTANCE, 1);
					effect(player, MobEffects.STRENGTH, 0);
					effect(player, MobEffects.FIRE_RESISTANCE, 0);
					effect(player, MobEffects.WATER_BREATHING, 0);
					effect(player, MobEffects.NIGHT_VISION, 0, 260);
				}
				if (wearing(player, ModItems.GALAXY_HELMET, ModItems.GALAXY_CHESTPLATE, ModItems.GALAXY_LEGGINGS, ModItems.GALAXY_BOOTS)) {
					effect(player, MobEffects.SPEED, 0);
					effect(player, MobEffects.NIGHT_VISION, 0, 260);
				}
				if (wearing(player, ModItems.PURPLE_HERO_HELMET, ModItems.PURPLE_HERO_CHESTPLATE, ModItems.PURPLE_HERO_LEGGINGS, ModItems.PURPLE_HERO_BOOTS)) {
					effect(player, MobEffects.SPEED, 2);
					effect(player, MobEffects.JUMP_BOOST, 2);
					effect(player, MobEffects.STRENGTH, 1);
					effect(player, MobEffects.NIGHT_VISION, 0, 260);
				}
			}
		});
	}

	private static void updateFlight(ServerPlayer player, boolean godlySet) {
		if (player.isCreative() || player.isSpectator()) {
			FLYERS.remove(player.getUUID());
			return;
		}
		if (godlySet) {
			if (!player.getAbilities().mayfly) {
				player.getAbilities().mayfly = true;
				player.onUpdateAbilities();
			}
			FLYERS.add(player.getUUID());
		} else if (FLYERS.remove(player.getUUID())) {
			player.getAbilities().mayfly = false;
			player.getAbilities().flying = false;
			player.onUpdateAbilities();
		}
	}

	private static boolean wearing(ServerPlayer player, Item head, Item chest, Item legs, Item feet) {
		return player.getItemBySlot(EquipmentSlot.HEAD).is(head)
				&& player.getItemBySlot(EquipmentSlot.CHEST).is(chest)
				&& player.getItemBySlot(EquipmentSlot.LEGS).is(legs)
				&& player.getItemBySlot(EquipmentSlot.FEET).is(feet);
	}

	private static void effect(ServerPlayer player, net.minecraft.core.Holder<net.minecraft.world.effect.MobEffect> effect, int amplifier) {
		effect(player, effect, amplifier, 40);
	}

	private static void effect(ServerPlayer player, net.minecraft.core.Holder<net.minecraft.world.effect.MobEffect> effect, int amplifier, int duration) {
		player.addEffect(new MobEffectInstance(effect, duration, amplifier, true, false));
	}
}
