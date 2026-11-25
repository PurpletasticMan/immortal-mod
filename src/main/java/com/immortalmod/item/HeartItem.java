package com.immortalmod.item;

import com.immortalmod.ModAttachments;
import net.fabricmc.fabric.api.attachment.v1.AttachmentType;
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

/** Right-click to permanently gain hearts of this item's kind (each kind has its own look in the heart bar). */
public class HeartItem extends Item {
	private final AttachmentType<Integer> kind;
	private final int hearts;

	public HeartItem(Properties properties, AttachmentType<Integer> kind, int hearts) {
		super(properties);
		this.kind = kind;
		this.hearts = hearts;
	}

	@Override
	public InteractionResult use(Level level, Player player, InteractionHand hand) {
		ItemStack stack = player.getItemInHand(hand);
		if (level instanceof ServerLevel serverLevel && player instanceof ServerPlayer serverPlayer) {
			ModAttachments.addHearts(serverPlayer, kind, hearts);
			serverLevel.sendParticles(ParticleTypes.HEART, player.getX(), player.getY() + 1.0, player.getZ(), 12 + hearts * 2, 0.5, 0.6, 0.5, 0.1);
			level.playSound(null, player.getX(), player.getY(), player.getZ(), SoundEvents.PLAYER_LEVELUP, SoundSource.PLAYERS, 1.0F, 1.3F);
			serverPlayer.sendSystemMessage(Component.literal("+" + hearts + " heart" + (hearts == 1 ? "" : "s")), true);
			stack.consume(1, player);
		}
		return InteractionResult.SUCCESS;
	}
}
