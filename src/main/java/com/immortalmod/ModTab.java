package com.immortalmod;

import net.fabricmc.fabric.api.creativetab.v1.CreativeModeTabEvents;
import net.fabricmc.fabric.api.creativetab.v1.FabricCreativeModeTab;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;

public final class ModTab {
	public static final ResourceKey<CreativeModeTab> TAB = ResourceKey.create(Registries.CREATIVE_MODE_TAB, ImmortalMod.id("main"));

	private ModTab() {
	}

	public static void init() {
		Registry.register(BuiltInRegistries.CREATIVE_MODE_TAB, TAB, FabricCreativeModeTab.builder()
				.icon(() -> new ItemStack(ModItems.GODLY_SWORD))
				.title(Component.translatable("itemGroup.immortal"))
				.build());
		CreativeModeTabEvents.modifyOutputEvent(TAB).register(entries -> {
			for (Item item : ModItems.ALL) {
				entries.accept(item);
			}
		});
	}
}
