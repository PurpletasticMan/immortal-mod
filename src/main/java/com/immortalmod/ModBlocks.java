package com.immortalmod;

import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;

public final class ModBlocks {
	/** A solid block that hurts anything touching its sides, top or bottom (see ModEvents). */
	public static class SwordBlock extends Block {
		public final float damage;

		public SwordBlock(BlockBehaviour.Properties properties, float damage) {
			super(properties);
			this.damage = damage;
		}
	}

	// spiky sword blocks: damage per hit, stronger each tier
	public static final Block IRON_SWORD_BLOCK = sword("iron_sword_block", 3.0F);
	public static final Block DIAMOND_SWORD_BLOCK = sword("diamond_sword_block", 5.0F);
	public static final Block NETHERITE_SWORD_BLOCK = sword("netherite_sword_block", 7.0F);
	public static final Block IMMORTAL_SWORD_BLOCK = sword("immortal_sword_block", 12.0F);
	public static final Block GODLY_SWORD_BLOCK = sword("godly_sword_block", 40.0F);

	// animated blocks, one per armour set
	public static final Block GALAXY_BLOCK = registerSet("galaxy_block", 5);
	public static final Block IMMORTAL_BLOCK = registerSet("immortal_block", 9);
	public static final Block GODLY_BLOCK = registerSet("godly_block", 15);

	// ores found in the End's outer islands
	public static final Block GALAXY_ORE = registerOre("galaxy_ore", 3);
	public static final Block IMMORTAL_ORE = registerOre("immortal_ore", 5);
	public static final Block GODLY_ORE = registerOre("godly_ore", 9);

	private ModBlocks() {
	}

	private static Block sword(String name, float damage) {
		ResourceKey<Block> key = ResourceKey.create(Registries.BLOCK, ImmortalMod.id(name));
		Block block = new SwordBlock(BlockBehaviour.Properties.of().strength(4.0F, 8.0F).sound(SoundType.METAL).setId(key), damage);
		return Registry.register(BuiltInRegistries.BLOCK, key, block);
	}

	private static Block registerSet(String name, int light) {
		ResourceKey<Block> key = ResourceKey.create(Registries.BLOCK, ImmortalMod.id(name));
		Block block = new Block(BlockBehaviour.Properties.of().strength(5.0F, 12.0F).sound(SoundType.METAL).lightLevel(state -> light).setId(key));
		return Registry.register(BuiltInRegistries.BLOCK, key, block);
	}

	private static Block registerOre(String name, int light) {
		ResourceKey<Block> key = ResourceKey.create(Registries.BLOCK, ImmortalMod.id(name));
		Block block = new Block(BlockBehaviour.Properties.of().strength(6.0F, 9.0F).sound(SoundType.STONE).requiresCorrectToolForDrops().lightLevel(state -> light).setId(key));
		return Registry.register(BuiltInRegistries.BLOCK, key, block);
	}

	public static void init() {
	}
}
