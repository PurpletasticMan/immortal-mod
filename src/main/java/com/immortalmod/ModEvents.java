package com.immortalmod;

import java.util.HashSet;
import java.util.Set;
import java.util.UUID;
import net.fabricmc.fabric.api.biome.v1.BiomeModifications;
import net.fabricmc.fabric.api.biome.v1.BiomeSelectors;
import net.fabricmc.fabric.api.entity.event.v1.ServerLivingEntityEvents;
import net.fabricmc.fabric.api.entity.event.v1.ServerPlayerEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.fabricmc.fabric.api.event.player.AttackBlockCallback;
import net.fabricmc.fabric.api.networking.v1.PayloadTypeRegistry;
import net.fabricmc.fabric.api.networking.v1.ServerPlayConnectionEvents;
import net.fabricmc.fabric.api.networking.v1.ServerPlayNetworking;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.util.Mth;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.biome.Biomes;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.GenerationStep;
import net.minecraft.world.phys.AABB;

public final class ModEvents {
	/** Players we gave flight to (so we only take it back from players we gave it to). */
	private static final Set<UUID> FLYERS = new HashSet<>();
	/** Players who have switched the Purple Hero chestplate on with the hotkey. */
	private static final Set<UUID> HERO_ACTIVE = new HashSet<>();

	private static final Set<Item> BEDROCK_BREAKERS = Set.of(ModItems.BEDROCK_PICKAXE, ModItems.IMMORTAL_PICKAXE, ModItems.GODLY_PICKAXE);

	private ModEvents() {
	}

	public static void init() {
		registerHearts();
		registerBedrockBreaking();
		registerTotems();
		registerArmourSets();
		registerHero();
		registerSwordBlocks();
		registerOres();
	}

	// ------------------------------------------------------------ hearts persist

	private static void registerHearts() {
		ServerPlayConnectionEvents.JOIN.register((handler, sender, server) -> ModAttachments.apply(handler.getPlayer()));
		ServerPlayerEvents.AFTER_RESPAWN.register((oldPlayer, newPlayer, alive) -> {
			ModAttachments.apply(newPlayer);
			newPlayer.setHealth(newPlayer.getMaxHealth());
		});
		ServerPlayerEvents.LEAVE.register(player -> {
			FLYERS.remove(player.getUUID());
			HERO_ACTIVE.remove(player.getUUID());
		});
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
				// purple hero chestplate: only while switched on with the hotkey
				if (HERO_ACTIVE.contains(player.getUUID())) {
					if (player.getItemBySlot(EquipmentSlot.CHEST).is(ModItems.PURPLE_HERO_CHESTPLATE)) {
						effect(player, MobEffects.SPEED, 2);
						effect(player, MobEffects.JUMP_BOOST, 2);
						effect(player, MobEffects.STRENGTH, 1);
						effect(player, MobEffects.RESISTANCE, 0);
						effect(player, MobEffects.NIGHT_VISION, 0, 260);
					} else {
						HERO_ACTIVE.remove(player.getUUID());
					}
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

	// ------------------------------------------------------------ hero hotkey

	private static void registerHero() {
		PayloadTypeRegistry.serverboundPlay().register(HeroTogglePayload.TYPE, HeroTogglePayload.CODEC);
		ServerPlayConnectionEvents.INIT.register((handler, server) -> ServerPlayNetworking.registerReceiver(handler, HeroTogglePayload.TYPE, ModEvents::onHeroToggle));
	}

	private static void onHeroToggle(HeroTogglePayload payload, ServerPlayNetworking.Context context) {
		ServerPlayer player = context.player();
		player.level().getServer().execute(() -> {
			if (!player.getItemBySlot(EquipmentSlot.CHEST).is(ModItems.PURPLE_HERO_CHESTPLATE)) {
				HERO_ACTIVE.remove(player.getUUID());
				player.sendSystemMessage(Component.literal("Wear the Purple Hero Chestplate first"), true);
				return;
			}
			boolean nowOn = HERO_ACTIVE.add(player.getUUID());
			if (!nowOn) {
				HERO_ACTIVE.remove(player.getUUID());
			}
			player.sendSystemMessage(Component.literal(nowOn ? "Purple Hero: ON" : "Purple Hero: OFF"), true);
		});
	}

	// ------------------------------------------------------------ spiky sword blocks

	private static void registerSwordBlocks() {
		ServerTickEvents.END_SERVER_TICK.register(server -> {
			if (server.getTickCount() % 4 != 0) {
				return;
			}
			Set<Integer> seen = new HashSet<>();
			for (ServerLevel level : server.getAllLevels()) {
				for (ServerPlayer player : level.players()) {
					for (LivingEntity entity : level.getEntitiesOfClass(LivingEntity.class, player.getBoundingBox().inflate(24.0))) {
						if (!entity.isAlive() || !seen.add(entity.getId())) {
							continue;
						}
						ModBlocks.SwordBlock touched = touchingSwordBlock(level, entity.getBoundingBox().inflate(0.06));
						if (touched != null) {
							entity.hurtServer(level, level.damageSources().cactus(), touched.damage);
						}
					}
				}
			}
		});
	}

	private static ModBlocks.SwordBlock touchingSwordBlock(ServerLevel level, AABB box) {
		BlockPos.MutableBlockPos pos = new BlockPos.MutableBlockPos();
		for (int x = Mth.floor(box.minX); x <= Mth.floor(box.maxX); x++) {
			for (int y = Mth.floor(box.minY); y <= Mth.floor(box.maxY); y++) {
				for (int z = Mth.floor(box.minZ); z <= Mth.floor(box.maxZ); z++) {
					if (level.getBlockState(pos.set(x, y, z)).getBlock() instanceof ModBlocks.SwordBlock sword) {
						return sword;
					}
				}
			}
		}
		return null;
	}

	// ------------------------------------------------------------ ores: End outer islands only (not the main island)

	private static void registerOres() {
		for (String name : new String[] {"galaxy_ore", "immortal_ore", "godly_ore"}) {
			BiomeModifications.addFeature(
					BiomeSelectors.includeByKey(Biomes.END_HIGHLANDS, Biomes.END_MIDLANDS, Biomes.END_BARRENS, Biomes.SMALL_END_ISLANDS),
					GenerationStep.Decoration.UNDERGROUND_ORES,
					ResourceKey.create(Registries.PLACED_FEATURE, ImmortalMod.id(name)));
		}
	}
}
