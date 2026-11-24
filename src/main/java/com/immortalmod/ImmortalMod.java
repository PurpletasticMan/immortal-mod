package com.immortalmod;

import net.fabricmc.api.ModInitializer;
import net.minecraft.resources.Identifier;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ImmortalMod implements ModInitializer {
	public static final String MOD_ID = "immortal";
	public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

	public static Identifier id(String path) {
		return Identifier.fromNamespaceAndPath(MOD_ID, path);
	}

	@Override
	public void onInitialize() {
		ModAttachments.init();
		ModBlocks.init();   // blocks first: the sword-block items need them
		ModItems.init();
		ModTab.init();
		ModEvents.init();
		LOGGER.info("Immortal & Godly loaded");
	}
}
