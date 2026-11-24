package com.immortalmod.item;

import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.projectile.Projectile;
import net.minecraft.world.entity.projectile.throwableitemprojectile.ThrownEnderpearl;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;

/** An ender pearl that is never used up and has no cooldown. */
public class InfinitePearlItem extends Item {
	private final float power;

	public InfinitePearlItem(Properties properties, float power) {
		super(properties);
		this.power = power;
	}

	@Override
	public InteractionResult use(Level level, Player player, InteractionHand hand) {
		ItemStack stack = player.getItemInHand(hand);
		level.playSound(null, player.getX(), player.getY(), player.getZ(), SoundEvents.ENDER_PEARL_THROW, SoundSource.NEUTRAL, 0.5F, 0.4F / (level.getRandom().nextFloat() * 0.4F + 0.8F));
		if (level instanceof ServerLevel serverLevel) {
			Projectile.spawnProjectileFromRotation(ThrownEnderpearl::new, serverLevel, stack.copyWithCount(1), player, 0.0F, power, 1.0F);
		}
		return InteractionResult.SUCCESS; // note: the stack is deliberately NOT shrunk and no cooldown is added
	}
}
