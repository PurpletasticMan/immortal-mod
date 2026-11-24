package com.immortalmod.item;

import com.immortalmod.ModAttachments;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;

/** Right-click to permanently gain extra max health. 1 heart = 2 half-hearts. */
public class HeartItem extends Item {
	private final int hearts;

	public HeartItem(Properties properties, int hearts) {
		super(properties);
		this.hearts = hearts;
	}

	@Override
	public InteractionResult use(Level level, Player player, InteractionHand hand) {
		ItemStack stack = player.getItemInHand(hand);
		if (level instanceof ServerLevel serverLevel && player instanceof ServerPlayer serverPlayer) {
			ModAttachments.addBonusHealth(serverPlayer, hearts * 2);
			serverLevel.sendParticles(ParticleTypes.HEART, player.getX(), player.getY() + 1.0, player.getZ(), 12 + hearts * 2, 0.5, 0.6, 0.5, 0.1);
			level.playSound(null, player.getX(), player.getY(), player.getZ(), SoundEvents.PLAYER_LEVELUP, SoundSource.PLAYERS, 1.0F, 1.3F);
			int total = serverPlayer.getAttachedOrCreate(ModAttachments.BONUS_HEALTH) / 2;
			serverPlayer.sendSystemMessage(Component.literal("+" + hearts + " heart" + (hearts == 1 ? "" : "s") + " (bonus hearts: " + total + ")"), true);
			stack.consume(1, player);
		}
		return InteractionResult.SUCCESS;
	}
}
