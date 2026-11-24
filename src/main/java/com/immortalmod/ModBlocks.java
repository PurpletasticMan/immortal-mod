package com.immortalmod;

import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;

public final class ModBlocks {
	public static final Block IRON_SWORD_BLOCK = register("iron_sword_block");
	public static final Block DIAMOND_SWORD_BLOCK = register("diamond_sword_block");
	public static final Block NETHERITE_SWORD_BLOCK = register("netherite_sword_block");
	public static final Block IMMORTAL_SWORD_BLOCK = register("immortal_sword_block");
	public static final Block GODLY_SWORD_BLOCK = register("godly_sword_block");

	private ModBlocks() {
	}

	private static Block register(String name) {
		ResourceKey<Block> key = ResourceKey.create(Registries.BLOCK, ImmortalMod.id(name));
		Block block = new Block(BlockBehaviour.Properties.of().strength(4.0F, 8.0F).sound(SoundType.METAL).setId(key));
		return Registry.register(BuiltInRegistries.BLOCK, key, block);
	}

	public static void init() {
	}
}
